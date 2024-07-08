from flask import request
from flask_socketio import emit, rooms

from src.api.extensions import socketio
from src.api.services.room import room_service
from src.api.services.participant import participant_service
from src.api.services.user import user_socket_session
from src.api.sockets.video_player.schemas import (
	PlayerStateSyncWithUserSchema, PlayerStateSyncWithEveryoneSchema, PlayerStateRequestSchema
)
from src.api.sockets.room.error import ROOM_SOCKET_ERRORS
from src.api.error.custom_error import ApiError


DEFAULT_PLAYER_STATE = {'currentTime': 0, 'isPaused': True}


@socketio.on('requestPlayerState')
def get_player_current_state(data):
	PlayerStateRequestSchema().validate(data)
	user_sid = request.sid
	user_id = user_socket_session.get(user_sid)
	room_id = data['roomId']

	if not room_service.is_field_exists('id', room_id):
		raise ApiError(ROOM_SOCKET_ERRORS['ROOM_NOT_FOUND'])

	user_rooms = rooms()
	if room_id not in user_rooms:
		raise ApiError(ROOM_SOCKET_ERRORS['USER_NOT_IN_ROOM'])

	participants = participant_service.get_room_participants(room_id)

	if len(participants) < 2:
		emit('syncPlayerState', DEFAULT_PLAYER_STATE, to=user_sid)
		return

	for participant in participants:
		if participant.userId != user_id:
			random_participant_user_id = participant.userId
			break

	random_participant_sid = user_socket_session.get(random_participant_user_id)
	emit('sendPlayerStateFromClient', {'userSID': user_sid}, to=random_participant_sid)


@socketio.on('sendPlayerStateToUser')
def send_player_current_state(data):
	PlayerStateSyncWithUserSchema().validate(data)

	user_sid = data['userSID']
	del data['userSID']

	emit('syncPlayerState', data, to=user_sid)


@socketio.on('sendPlayerStateToEveryone')
def sync_player_current_state(data):
	PlayerStateSyncWithEveryoneSchema().validate(data)

	room_id = data['roomId']
	del data['roomId']

	if not room_service.is_field_exists('id', room_id):
		raise ApiError(ROOM_SOCKET_ERRORS['ROOM_NOT_FOUND'])

	user_rooms = rooms()
	if room_id not in user_rooms:
		raise ApiError(ROOM_SOCKET_ERRORS['USER_NOT_IN_ROOM'])

	emit('syncPlayerState', data, to=room_id, include_self=False)

	return 200