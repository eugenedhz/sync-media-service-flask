from flask import request

from flask_socketio import emit

from src.api.extensions import socketio
from src.api.services.room import room_service
from src.api.services.media import media_service
from src.api.services.playlist_media import playlist_media_service
from src.api.sockets.playlist_media.schemas import (
	CreatePlaylistMediaSchema, UpdatePlaylistMediaSchema, PlaylistMediaIdSchema
)
from src.usecase.playlist_media.dto import PlaylistMediaCreateDTO, PlaylistMediaUpdateDTO
from src.api.routes.room.error import ROOM_API_ERRORS
from src.api.routes.media.error import MEDIA_API_ERRORS
from src.api.sockets.playlist_media.error import PLAYLIST_MEDIA_SOCKET_ERRORS
from src.api.error.custom_error import ApiError


@socketio.on('addPlaylistMedia')
def create_playlist_media(data):
	CreatePlaylistMediaSchema().validate(data)

	is_room_exist = room_service.is_field_exists('id', data['roomId'])
	if not is_room_exist:
		raise ApiError(ROOM_API_ERRORS['ROOM_NOT_FOUND'])

	is_media_exist = media_service.is_field_exists('id', data['mediaId'])
	if not is_media_exist:
		raise ApiError(MEDIA_API_ERRORS['MEDIA_NOT_FOUND'])

	found_playlist_media = playlist_media_service.get_playlist_media_by_room_and_media_id(
		room_id = data['roomId'],
		media_id = data['mediaId']
	)

	if found_playlist_media != None:
		raise ApiError(PLAYLIST_MEDIA_SOCKET_ERRORS['PLAYLIST_MEDIA_ALREADY_IN_ROOM'])

	dto = PlaylistMediaCreateDTO(**data)
	playlist_media = playlist_media_service.create_playlist_media(dto)

	emit('playlistMediaAdded', playlist_media._asdict(), to=playlist_media.roomId)


@socketio.on('updatePlaylistMedia')
def update_playlist_media(data):
	UpdatePlaylistMediaSchema().validate(data)

	playlist_media_id = data['playlistMediaId']
	del data['playlistMediaId']

	is_playlist_media_exist = playlist_media_service.is_field_exists('id', playlist_media_id)
	if not is_playlist_media_exist:
		raise ApiError(PLAYLIST_MEDIA_API_ERRORS['PLAYLIST_MEDIA_NOT_FOUND'])

	is_order_equals_zero = False

	if 'order' in request.json:
		if playlist_media.order == data['order']:
			raise ApiError(PLAYLIST_MEDIA_SOCKET_ERRORS['SAME_PLAYLIST_MEDIA_ORDER'])

		max_playlist_order = playlist_media_service.get_max_playlist_order()
		if data['order'] > max_playlist_order:
			raise ApiError(PLAYLIST_MEDIA_SOCKET_ERRORS['PLAYLIST_ORDER_OUT_OF_RANGE'])

	dto = PlaylistMediaUpdateDTO(**data)
	playlist_media = playlist_media_service.update_playlist_media(
		id = playlist_media_id,
		update_playlist_media_dto = dto
	)

	emit('playlistMediaUpdated', playlist_media._asdict(), to=playlist_media.roomId)


@socketio.on('setPlaylistMediaToPlayer')
def update_playlist_media(data):
	PlaylistMediaIdSchema().validate(data)
	playlist_media_id = data['playlistMediaId']

	is_playlist_media_exist = playlist_media_service.is_field_exists('id', playlist_media_id)
	if not is_playlist_media_exist:
		raise ApiError(PLAYLIST_MEDIA_SOCKET_ERRORS['PLAYLIST_MEDIA_NOT_FOUND'])

	playlist_media_in_player = playlist_media_service.get_playlist_media_by_order(0)
	if playlist_media_in_player.id == playlist_media_id:
		raise ApiError(PLAYLIST_MEDIA_SOCKET_ERRORS['PLAYLIST_MEDIA_ALREADY_IN_PLAYER'])

	playlist_media_service.delete_playlist_media(
		playlist_media_in_player.id
	)

	dto = PlaylistMediaUpdateDTO(order=0)
	playlist_media = playlist_media_service.update_playlist_media(
		id = playlist_media_id,
		update_playlist_media_dto = dto
	)

	emit('playlistMediaSettedToPlayer', playlist_media._asdict(), to=playlist_media.roomId)


@socketio.on('deletePlaylistMedia')
def delete_playlist_media(data):
	PlaylistMediaIdSchema().validate(data)
	playlist_media_id = data['playlistMediaId']

	is_playlist_media_exist = playlist_media_service.is_field_exists('id', playlist_media_id)
	if not is_playlist_media_exist:
		raise ApiError(PLAYLIST_MEDIA_SOCKET_ERRORS['PLAYLIST_MEDIA_NOT_FOUND'])

	playlist_media = playlist_media_service.delete_playlist_media(
		id = playlist_media_id
	)

	emit('playlistMediaDeleted', playlist_media._asdict(), to=playlist_media.roomId)
