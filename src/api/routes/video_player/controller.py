from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_socketio import emit

from src.app import app
from src.api.services.room import room_service
from src.api.services.participant import participant_service
from src.api.services.user import user_socket_session
from src.api.routes.video_player.schemas import VideoPlayerStateSchema
from src.api.error.shared_error import API_ERRORS
from src.api.routes.room.error import ROOM_API_ERRORS
from src.api.error.custom_error import ApiError


DEFAULT_PLAYER_STATE = {'currentTime': 0, 'isPaused': True}


@app.route('/player/request_current_state', methods=['POST'])
@jwt_required()
def get_player_current_state():
	user_id = int(get_jwt_identity())
	user_sid = user_socket_session.get(requesting_user_id)

	if user_sid is None:
		raise ApiError(API_ERRORS['USER_SOCKET_SESSION_NOT_FOUND'])

	room_id = request.args.get('roomId')
	if room_id is None:
		raise ApiError(API_ERRORS['NO_IDENTITY_PROVIDED'])

	if not room_service.is_field_exists('id', room_id):
		raise ApiError(ROOM_API_ERRORS['ROOM_NOT_FOUND'])

	participants = participant_service.get_room_participants(room_id)

	if len(participants) < 2:
		emit('getVideoPlayerCurrentState', DEFAULT_PLAYER_STATE, to=requesting_user_sid, namespace='/')
		return 200

	for participant in participants:
		if participant.userId != user_id:
			random_participant_user_id = participant.userId

	random_user_sid = user_socket_session.get(random_participant_user_id)
	emit('sendVideoPlayerCurrentState', {'userSID': requesting_user_sid}, to=random_user_sid, namespace='/')

	return 200


@app.route('/player/send_current_state', methods=['POST'])
@jwt_required()
def get_player_current_state():
	user_sid = request.args.get('userSID')
	VideoPlayerStateSchema().validate(request.json)

	emit('getVideoPlayerCurrentState', request.json, to=user_sid, namespace='/')

	return 200


@app.route('/player/sync', methods=['POST'])
@jwt_required()
def get_player_current_state():
	VideoPlayerStateSchema().validate(request.json)

	room_id = request.args.get('roomId')
	if room_id is None:
		raise ApiError(API_ERRORS['NO_IDENTITY_PROVIDED'])

	if not room_service.is_field_exists('id', room_id):
		raise ApiError(ROOM_API_ERRORS['ROOM_NOT_FOUND'])

	emit('getVideoPlayerCurrentState', request.json, to=room_id, namespace='/')

	return 200