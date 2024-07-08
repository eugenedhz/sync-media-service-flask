from flask import request, jsonify

from src.app import app
from src.domain.playlist_media import PlaylistMedia
from src.api.services.playlist_media import playlist_media_service
from src.api.routes.playlist_media.schemas import PlaylistMediaSchema
from src.usecase.playlist_media.dto import PlaylistMediaDTO
from src.usecase.dto import QueryParametersDTO
from src.api.error.shared_error import API_ERRORS
from src.api.routes.playlist_media.error import PLAYLIST_MEDIA_API_ERRORS
from src.api.error.custom_error import ApiError

from pkg.query_params.select.parse import parse_select
from pkg.query_params.filter_by.parse import parse_filter_by


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

	limit = request_params.get('limit')
	offset = request_params.get('offset')
	if limit or offset:
		try:
			limit = int(limit)
			offset = int(offset)
		except:
			raise ApiError(API_ERRORS['INVALID_PAGE_QUERY'])

	query_parameters_dto = QueryParametersDTO(filters=filter_by, limit=limit, offset=offset)
	playlist_medias = playlist_media_service.get_playlist_medias(query_parameters_dto=query_parameters_dto)

	if len(playlist_medias) == 0:
		return jsonify([])

	serialize_playlist_medias = PlaylistMediaSchema(only=select, many=True).dump

	return jsonify(serialize_playlist_medias(playlist_medias))
