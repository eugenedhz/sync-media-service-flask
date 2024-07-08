from flask import request
from flask_socketio import emit

from src.api.extensions import socketio
from src.api.services.room import room_service
from src.api.services.participant import participant_service
from src.api.services.user import user_socket_session
from src.api.sockets.chat.schemas import MessageSchema
from src.api.sockets.room.error import ROOM_SOCKET_ERRORS
from src.api.error.custom_error import ApiError


@socketio.on('sendMessage')
def message_event(data):
	MessageSchema().validate(data)
	user_id = user_socket_session.get(request.sid)
	room_id = data['roomId']

	if not room_service.is_field_exists('id', room_id):
		raise ApiError(ROOM_SOCKET_ERRORS['ROOM_NOT_FOUND'])

	participant = participant_service.get_participant_by_user_and_room_id(
		user_id = user_id,
		room_id = room_id
	)

	if not participant:
		raise ApiError(ROOM_SOCKET_ERRORS['USER_NOT_IN_ROOM'])

	del data['roomId']
	data['participant'] = participant._asdict()

	emit('messageSent', data, to=room_id)
