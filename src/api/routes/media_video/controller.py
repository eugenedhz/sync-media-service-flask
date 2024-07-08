from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from pycountry import countries

from src.app import app
from src.api.services.media_video import media_video_service
from src.api.services.media import media_service
from src.api.services.video import video_service
from src.api.routes.media_video.schemas import (
    MediaVideoSchema, CreateMediaVideoSchema, UpdateMediaVideoSchema
)
from src.usecase.media_video.dto import MediaVideoDTO, MediaVideoCreateDTO, MediaVideoUpdateDTO
from src.usecase.dto import QueryParametersDTO
from src.api.error.shared_error import API_ERRORS
from src.api.routes.media_video.error import MEDIA_VIDEO_API_ERRORS
from src.api.routes.media.error import MEDIA_API_ERRORS
from src.api.routes.video.error import VIDEO_API_ERRORS
from src.api.error.custom_error import ApiError
from src.api.helpers.video import concat_video_to_url, delete_videos_with_quality
from src.api.helpers.jwt import role_required

from src.configs.constants import Static, Role

from pkg.query_params.select.parse import parse_select
from pkg.query_params.filter_by.parse import parse_filter_by
from pkg.query_params.expand.parse import parse_expand
from pkg.file.filename import split_filename


EXPAND_FIELDS = ('media',)


@app.route('/media/video', methods=['POST'])
@jwt_required()
@role_required(Role.ADMIN)
def create_video():
    json = request.json
    CreateMediaVideoSchema().validate(json)

    is_media_exists = media_service.is_field_exists('id', json['mediaId'])
    if not is_media_exists:
        raise ApiError(MEDIA_API_ERRORS['MEDIA_NOT_FOUND'])

    is_language_exists = countries.get(alpha_2=json['language'])
    if not is_language_exists:
        raise ApiError(MEDIA_VIDEO_API_ERRORS['LANGUAGE_NOT_FOUND'])

    name = split_filename(json['source']).name
    if video_service.find(name) is None:
        raise ApiError(VIDEO_API_ERRORS['VIDEO_NOT_FOUND'])

    json['source'] = concat_video_to_url(json['source'])
    is_source_exists = media_video_service.is_field_exists('source', json['source'])
    if is_source_exists:
        raise ApiError(MEDIA_VIDEO_API_ERRORS['SOURCE_EXISTS'])

    dto = MediaVideoCreateDTO(**json)
    created_media_video = media_video_service.create_video(dto)

    return jsonify(created_media_video._asdict())


@app.route('/media/video', methods=['GET'])
def get_video_by_id():
    request_params = request.args
    video_id = request_params.get('id')

    if video_id is None:
        raise ApiError(API_ERRORS['NO_IDENTITY_PROVIDED'])
    if not video_id.isdigit():
        raise ApiError(API_ERRORS['INVALID_ID'])

    expand = request_params.get('expand')
    try:
        expand = parse_expand(expand=expand, valid_fields=EXPAND_FIELDS)
    except:
        raise ApiError(API_ERRORS['INVALID_EXPAND'])

    select = request_params.get('select')
    video_fields = MediaVideoDTO.__match_args__
    try:
        select = parse_select(select=select, valid_fields=video_fields)
    except:
        raise ApiError(API_ERRORS['INVALID_SELECT'])

    media_video = media_video_service.get_video_by_id(video_id)
    if media_video is None:
        raise ApiError(MEDIA_VIDEO_API_ERRORS['MEDIA_VIDEO_NOT_FOUND'])

    serialize_media_video = MediaVideoSchema(only=select).dump
    serialized_media_video = serialize_media_video(media_video)

    if not expand:
        return jsonify(serialized_media_video)

    if 'media' in expand:
        media = media_service.get_by_id(media_video.mediaId)
        serialized_media_video['media'] = media._asdict()
    
    return jsonify(serialized_media_video)


@app.route('/media/video/all', methods=['GET'])
def get_all_videos():
    request_params = request.args

    select = request_params.get('select')
    filter_by = request_params.get('filter_by')

    expand = request_params.get('expand')
    try:
        expand = parse_expand(expand=expand, valid_fields=EXPAND_FIELDS)
    except:
        raise ApiError(API_ERRORS['INVALID_EXPAND'])

    video_fields = MediaVideoDTO.__match_args__
    try:
        select = parse_select(select=select, valid_fields=video_fields)
    except:
        raise ApiError(API_ERRORS['INVALID_SELECT'])

    video_fields = MediaVideoDTO.__annotations__
    try:
        filter_by = parse_filter_by(filter_query=filter_by, valid_fields=video_fields)
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
    media_videos = media_video_service.get_videos(query_parameters_dto)

    if len(media_videos) == 0:
        return jsonify([])

    serialize_media_videos = MediaVideoSchema(only=select, many=True).dump
    serialized_media_videos = serialize_media_videos(media_videos)

    if not expand:
        return jsonify(serialized_media_videos)

    if 'media' in expand:
        for i in range(len(media_videos)):
            media_id = media_videos[i].mediaId
            media = media_service.get_by_id(media_id)
            serialized_media_videos[i]['media'] = media._asdict()

    return jsonify(serialized_media_videos)


@app.route('/media/video', methods=['PATCH'])
@jwt_required()
@role_required(Role.ADMIN)
def update_video():
    video_id = request.args.get('id')

    if video_id is None:
        raise ApiError(API_ERRORS['NO_IDENTITY_PROVIDED'])
    if not video_id.isdigit():
        raise ApiError(API_ERRORS['INVALID_ID'])

    json = request.json
    UpdateMediaVideoSchema().validate(json)

    media_video = media_video_service.get_video_by_id(video_id)
    if media_video is None:
        raise ApiError(MEDIA_VIDEO_API_ERRORS['MEDIA_VIDEO_NOT_FOUND'])

    if 'language' in json:
        is_language_exists = countries.get(alpha_2=json['language'])
        if not is_language_exists:
            raise ApiError(MEDIA_VIDEO_API_ERRORS['LANGUAGE_NOT_FOUND'])

    if 'source' in json:
        name = split_filename(json['source']).name
        if video_service.find(name) is None:
            raise ApiError(VIDEO_API_ERRORS['VIDEO_NOT_FOUND'])

        json['source'] = concat_video_to_url(json['source'])
        is_source_exists = media_video_service.is_field_exists('source', json['source'])
        if is_source_exists:
            raise ApiError(MEDIA_VIDEO_API_ERRORS['SOURCE_EXISTS'])
            
        delete_videos_with_quality(media_video.source)

    dto = MediaVideoUpdateDTO(**json)
    updated_media_video = media_video_service.update_video(id=video_id, update_video_dto=dto)

    return jsonify(updated_media_video._asdict())


@app.route('/media/video', methods=['DELETE'])
@jwt_required()
@role_required(Role.ADMIN)
def delete_video():
    video_id = request.args.get('id')

    if video_id is None:
        raise ApiError(API_ERRORS['NO_IDENTITY_PROVIDED'])
    if not video_id.isdigit():
        raise ApiError(API_ERRORS['INVALID_ID'])

    video_id = int(video_id)
    media_video = media_video_service.get_video_by_id(video_id)
    if media_video is None:
        raise ApiError(MEDIA_VIDEO_API_ERRORS['MEDIA_VIDEO_NOT_FOUND'])

    media_video_service.delete_video(video_id)
    delete_videos_with_quality(media_video.source)

    return jsonify(media_video._asdict())
