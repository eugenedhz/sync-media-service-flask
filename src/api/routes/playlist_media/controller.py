from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from flask_socketio import emit

from src.app import app
from src.domain.playlist_media import PlaylistMedia
from src.api.services.room import room_service
from src.api.services.media import media_service
from src.api.services.participant import participant_service
from src.api.services.playlist_media import playlist_media_service
from src.api.routes.playlist_media.schemas import (
	PlaylistMediaSchema, CreatePlaylistMediaSchema, UpdatePlaylistMediaSchema
)
from src.usecase.playlist_media.dto import PlaylistMediaDTO, PlaylistMediaCreateDTO, PlaylistMediaUpdateDTO
from src.usecase.dto import QueryParametersDTO
from src.api.error.shared_error import API_ERRORS
from src.api.routes.playlist_media.error import PLAYLIST_MEDIA_API_ERRORS
from src.api.routes.room.error import ROOM_API_ERRORS
from src.api.routes.media.error import MEDIA_API_ERRORS
from src.api.error.custom_error import ApiError

from pkg.query_params.select.parse import parse_select
from pkg.query_params.filter_by.parse import parse_filter_by


@app.route('/playlist_media', methods=['POST'])
@jwt_required()
def create_playlist_media():
	CreatePlaylistMediaSchema().validate(request.json)
	json = request.json

	is_room_exist = room_service.is_field_exists('id', json['roomId'])
	if not is_room_exist:
		raise ApiError(ROOM_API_ERRORS['ROOM_NOT_FOUND'])

	is_media_exist = media_service.is_field_exists('id', json['mediaId'])
	if not is_media_exist:
		raise ApiError(MEDIA_API_ERRORS['MEDIA_NOT_FOUND'])

	found_playlist_media = playlist_media_service.get_playlist_media_by_room_and_media_id(
		room_id = json['roomId'],
		media_id = json['mediaId']
	)

	if found_playlist_media != None:
		raise ApiError(PLAYLIST_MEDIA_API_ERRORS['PLAYLIST_MEDIA_ALREADY_IN_ROOM'])

	dto = PlaylistMediaCreateDTO(**json)
	playlist_media = playlist_media_service.create_playlist_media(dto)

	emit('mediaAdded', playlist_media._asdict(), to=playlist_media.roomId, namespace='/')

	return jsonify(playlist_media._asdict())


@app.route('/playlist_media', methods=['GET'])
def get_playlist_media():
	playlist_media_id = request.args.get('id')
	media_id = request.args.get('mediaId')
	room_id = request.args.get('roomId')

	if not(playlist_media_id) and not(media_id and room_id):
		raise ApiError(API_ERRORS['NO_IDENTITY_PROVIDED'])

	select = request.args.get('select')
	playlist_media_fields = PlaylistMediaDTO.__match_args__
	try:
		select = parse_select(select=select, valid_fields=playlist_media_fields)
	except:
		raise ApiError(API_ERRORS['INVALID_SELECT'])

	if playlist_media_id:
		playlist_media = playlist_media_service.get_playlist_media_by_id(
			playlist_media_id
		)
	else:
		playlist_media = playlist_media_service.get_playlist_media_by_room_and_media_id(
			room_id = room_id,
			media_id = media_id
		)

	if playlist_media is None:
		raise ApiError(PLAYLIST_MEDIA_API_ERRORS['PLAYLIST_MEDIA_NOT_FOUND'])

	serialize_playlist_media = PlaylistMediaSchema(only=select).dump

	return jsonify(serialize_playlist_media(playlist_media))


@app.route('/playlist_media/all', methods=['GET'])
def get_all_playlist_media():
	request_params = request.args

	select = request_params.get('select')
	filter_by = request_params.get('filter_by')

	playlist_media_fields = PlaylistMediaDTO.__match_args__
	try:
		select = parse_select(select=select, valid_fields=playlist_media_fields)
	except:
		raise ApiError(API_ERRORS['INVALID_SELECT'])

	playlist_media_fields = PlaylistMedia.__annotations__
	try:
		filter_by = parse_filter_by(filter_query=filter_by, valid_fields=playlist_media_fields)
	except:
		raise ApiError(API_ERRORS['INVALID_FILTERS'])

	query_parameters_dto = QueryParametersDTO(filters=filter_by)
	playlist_medias = playlist_media_service.get_playlist_medias(query_parameters_dto=query_parameters_dto)

	if len(playlist_medias) == 0:
		raise ApiError(PLAYLIST_MEDIA_API_ERRORS['PLAYLIST_MEDIAS_NOT_FOUND'])

	serialize_playlist_medias = PlaylistMediaSchema(only=select, many=True).dump

	return jsonify(serialize_playlist_medias(playlist_medias))


@app.route('/playlist_media', methods=['PATCH'])
def update_playlist_media():
	playlist_media_id = request.args.get('id')

	if not playlist_media_id:
		raise ApiError(API_ERRORS['NO_IDENTITY_PROVIDED'])

	UpdatePlaylistMediaSchema().validate(request.json)

	playlist_media = playlist_media_service.get_playlist_media_by_id(playlist_media_id)
	if playlist_media is None:
		raise ApiError(PLAYLIST_MEDIA_API_ERRORS['PLAYLIST_MEDIA_NOT_FOUND'])

	is_order_equals_zero = False

	if 'order' in request.json:
		if playlist_media.order == request.json['order']:
			raise ApiError(PLAYLIST_MEDIA_API_ERRORS['SAME_PLAYLIST_MEDIA_ORDER'])

		max_playlist_order = playlist_media_service.get_max_playlist_order()

		if request.json['order'] > max_playlist_order:
			raise ApiError(PLAYLIST_MEDIA_API_ERRORS['PLAYLIST_ORDER_OUT_OF_RANGE'])

		if request.json['order'] == 0:
			is_order_equals_zero = True

	if is_order_equals_zero:
		playlist_media_in_player = playlist_media_service.get_playlist_media_by_order(0)

		playlist_media_service.delete_playlist_media(
			playlist_media_in_player.id
		)

	dto = PlaylistMediaUpdateDTO(**request.json)
	playlist_media = playlist_media_service.update_playlist_media(
		id = playlist_media_id,
		update_playlist_media_dto = dto
	)

	if is_order_equals_zero:
		emit('mediaSetToPlayer', playlist_media._asdict(), to=playlist_media.roomId, namespace='/')
	else:
		emit('mediaUpdated', playlist_media._asdict(), to=playlist_media.roomId, namespace='/')

	return jsonify(playlist_media._asdict())


@app.route('/playlist_media', methods=['DELETE'])
def delete_playlist_media():
	playlist_media_id = request.args.get('id')

	if not playlist_media_id:
		raise ApiError(API_ERRORS['NO_IDENTITY_PROVIDED'])

	is_playlist_media_exist = playlist_media_service.is_field_exists('id', playlist_media_id)
	if not is_playlist_media_exist:
		raise ApiError(PLAYLIST_MEDIA_API_ERRORS['PLAYLIST_MEDIA_NOT_FOUND'])

	playlist_media = playlist_media_service.delete_playlist_media(
		id = playlist_media_id
	)

	emit('mediaDeleted', playlist_media._asdict(), to=playlist_media.roomId, namespace='/')

	return jsonify(playlist_media._asdict())
