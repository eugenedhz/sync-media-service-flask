from flask_socketio import (
	ConnectionRefusedError, emit, rooms, leave_room, disconnect
)
from flask_jwt_extended import decode_token
from flask import request

from src.api.extensions import socketio
from src.api.services.participant import participant_service
from src.api.services.user import user_socket_session


@socketio.on('connect')
def connect_event():
	try:
		tokens = request.headers['Cookie'].split(';')
		access_token = ''
		for token in tokens:
			if 'access_token_cookie' in token:
				access_token = token.replace('access_token_cookie=', '').strip()
				break
		payload = decode_token(access_token)
	except Exception as e:
		raise ConnectionRefusedError('ACCESS_TOKEN_REQUIRED')

	user_id = int(payload['sub'])
	
	current_user_sid = user_socket_session.get(user_id)
	if current_user_sid:
		disconnect(current_user_sid)

	user_socket_session.set(request.sid, user_id)
	user_socket_session.set(user_id, request.sid)

	emit('connected', {'userId': user_id})


@socketio.on('disconnect')
def disconnect_event():
	user_id = user_socket_session.get(request.sid)
	if user_id is None:
		return

	user_rooms = rooms()
	for room in user_rooms:
		if isinstance(room, int):
			participant = participant_service.get_participant_by_user_and_room_id(
				user_id = user_id,
				room_id = room
			)
			if participant:
				emit('left', participant._asdict(), to=room)
				participant_service.delete_participant(participant.id)

	user_socket_session.delete(request.sid)
	user_socket_session.delete(user_id)
