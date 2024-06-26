from flask_socketio import send, emit, join_room, leave_room
from flask import request

from src.api.extensions import socketio
from src.api.services.room import room_service
from src.api.services.participant import participant_service
from src.api.services.user import user_socket_session
from src.usecase.participant.dto import ParticipantCreateDTO
from src.api.error.custom_error import ApiError
from src.api.sockets.room.schemas import JoinAndLeaveRoomSchema
from src.api.sockets.room.error import ROOM_SOCKET_ERRORS


@socketio.on('join')
def join_room_event(data):
	JoinAndLeaveRoomSchema().validate(data)
	user_id = user_socket_session.get(request.sid)
	room_id = data['roomId']

	is_room_exists = room_service.is_field_exists('id', room_id)
	if not is_room_exists:
		raise ApiError(ROOM_SOCKET_ERRORS['ROOM_NOT_FOUND'])

	is_participating = participant_service.is_field_exists('userId', user_id)
	if is_participating:
		raise ApiError(ROOM_SOCKET_ERRORS['USER_ALREADY_IN_SOME_ROOM'])

	participant_dto = ParticipantCreateDTO(userId=user_id, roomId=room_id)
	participant = participant_service.create_participant(participant_dto)

	emit('joined', participant._asdict(), to=room_id)
	join_room(room_id)


@socketio.on('leave')
def leave_room_event(data):
	JoinAndLeaveRoomSchema().validate(data)
	user_id = user_socket_session.get(request.sid)
	room_id = data['roomId']

	is_room_exists = room_service.is_field_exists('id', room_id)
	if not is_room_exists:
		raise ApiError(ROOM_SOCKET_ERRORS['ROOM_NOT_FOUND'])

	participant = participant_service.get_participant_by_user_and_room_id(
		user_id = user_id,
		room_id = room_id
	)
	if participant is None:
		raise ApiError(ROOM_SOCKET_ERRORS['USER_NOT_IN_ROOM'])

	participant_service.delete_participant(participant.id)
	leave_room(room_id)

	emit('left', participant._asdict(), to=room_id)