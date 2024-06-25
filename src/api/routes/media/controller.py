from flask import request, jsonify
from flask_jwt_extended import jwt_required

from src.app import app
from src.api.services.media import media_service
from src.api.services.media_video import media_video_service
from src.api.services.genre import genre_service
from src.api.services.image import image_service
from src.api.services.video import video_service
from src.usecase.dto import QueryParametersDTO
from src.usecase.media.dto import MediaDTO, MediaUpdateDTO, MediaCreateDTO
from src.api.error.shared_error import API_ERRORS
from src.api.routes.media.error import MEDIA_API_ERRORS
from src.api.routes.video.error import VIDEO_API_ERRORS
from src.api.error.custom_error import ApiError
from src.api.routes.genre.schemas import GenreSchema
from src.api.routes.media.schemas import (
    MediaSchema, UpdateMediaSchema, CreateMediaSchema,
    UpdateMediaFilesSchema, CreateMediaFilesSchema
)
from src.api.routes.media_video.schemas import MediaVideoSchema
from src.configs.constants import Static
from src.api.helpers.video import concat_video_to_url, delete_videos_with_quality

from pkg.query_params.select.parse import parse_select
from pkg.query_params.filter_by.parse import parse_filter_by
from pkg.query_params.expand.parse import parse_expand
from pkg.file.image.jpg_validate import is_valid_jpg
from pkg.file.filename import split_filename
from pkg.dict.keys import find_keys


FILES = ('preview', 'thumbnail')
EXPAND_FIELDS = ('genres', 'videos')


@app.route('/media', methods=['POST'])
@jwt_required()
def media_create():
    CreateMediaFilesSchema().validate(request.files)
    formdata = CreateMediaSchema().load(request.form)

    for key, image in request.files.items():
        data = image.read()
        extension = split_filename(image.filename).extension

        if not is_valid_jpg(data, extension):
            raise ApiError(API_ERRORS['INVALID_JPG'])

        try:
            saved_filename = image_service.save(data=data, extension=extension)
        except:
            raise ApiError(API_ERRORS['CANT_SAVE_FILE'])

        image_url = Static.IMAGES_URL + saved_filename
        formdata[key] = image_url

    if 'trailer' in formdata:
        name = split_filename(formdata['trailer']).name
        if video_service.find(name) is None:
            raise ApiError(VIDEO_API_ERRORS['VIDEO_NOT_FOUND'])

        formdata['trailer'] = concat_video_to_url(formdata['trailer'])

    dto = MediaCreateDTO(**formdata)
    created_media = media_service.create_media(dto)

    return jsonify(created_media._asdict())


@app.route('/media', methods=['GET'])
def get_media_by_id():
    request_params = request.args

    media_id = request_params.get('id')

    if media_id is None:
        raise ApiError(API_ERRORS['NO_IDENTITY_PROVIDED'])

    if not media_id.isdigit():
        raise ApiError(API_ERRORS['INVALID_ID'])

    expand = request_params.get('expand')
    try:
        expand = parse_expand(expand=expand, valid_fields=EXPAND_FIELDS)
    except:
        raise ApiError(API_ERRORS['INVALID_EXPAND'])

    select = request_params.get('select')
    media_fields = MediaDTO.__match_args__
    try:
        select = parse_select(select=select, valid_fields=media_fields)
    except:
        raise ApiError(API_ERRORS['INVALID_SELECT'])

    media = media_service.get_by_id(id=media_id)

    if media is None:
        raise ApiError(MEDIA_API_ERRORS['MEDIA_NOT_FOUND'])

    serialize_media = MediaSchema(only=select).dump
    serialized_media = serialize_media(media)

    if not expand:
        return jsonify(serialized_media)

    if 'videos' in expand:
        serialize_media_videos = MediaVideoSchema(only=select, many=True).dump
        videos = media_video_service.get_media_videos(media.id)
        serialized_media['videos'] = serialize_media_videos(videos)

    if 'genres' in expand:
        serialize_genres = GenreSchema(many=True).dump
        genres = genre_service.get_media_genres(media.id)
        serialized_media['genres'] = serialize_genres(genres)

    return jsonify(serialized_media)


@app.route('/media/all', methods=['GET'])
def get_all_medias():
    request_params = request.args

    select = request_params.get('select')
    filter_by = request_params.get('filter_by')
    expand = request_params.get('expand')

    try:
        expand = parse_expand(expand=expand, valid_fields=EXPAND_FIELDS)
    except:
        raise ApiError(API_ERRORS['INVALID_EXPAND'])

    media_fields = MediaDTO.__match_args__
    try:
        select = parse_select(select=select, valid_fields=media_fields)
    except:
        raise ApiError(API_ERRORS['INVALID_SELECT'])

    media_fields = MediaDTO.__annotations__
    try:
        filter_by = parse_filter_by(filter_query=filter_by, valid_fields=media_fields)
    except:
        raise ApiError(API_ERRORS['INVALID_FILTERS'])

    expand = request_params.get('expand')
    try:
        expand = parse_expand(expand=expand, valid_fields=EXPAND_FIELDS)
    except:
        raise ApiError(API_ERRORS['INVALID_EXPAND'])

    query_parameters_dto = QueryParametersDTO(filters=filter_by)
    medias = media_service.get_medias(query_parameters_dto=query_parameters_dto)

    if len(medias) == 0:
        raise ApiError(MEDIA_API_ERRORS['MEDIAS_NOT_FOUND'])

    serialize_medias = MediaSchema(only=select, many=True).dump
    serialized_medias = serialize_medias(medias)

    if not expand:
        return jsonify(serialized_medias)

    if 'videos' in expand:
        serialize_media_videos = MediaVideoSchema(many=True).dump
        for i in range(len(medias)):
            videos = media_video_service.get_media_videos(medias[i].id)
            serialized_medias[i]['videos'] = serialize_media_videos(videos)

    if 'genres' in expand:
        serialize_genres = GenreSchema(many=True).dump
        for i in range(len(medias)):
            media_id = medias[i].id
            genres = genre_service.get_media_genres(media_id)
            serialized_medias[i]['genres'] = serialize_genres(genres)

    return jsonify(serialized_medias)


@app.route('/media', methods=['PATCH'])
@jwt_required()
def update_media():
    media_id = request.args.get('id')

    if media_id is None:
        raise ApiError(API_ERRORS['NO_IDENTITY_PROVIDED'])

    if not media_id.isdigit():
        raise ApiError(API_ERRORS['INVALID_ID'])

    UpdateMediaFilesSchema().validate(request.files)
    formdata = UpdateMediaSchema().load(request.form)

    files = find_keys(request.files, FILES)

    if len(formdata) == 0 and not files:
        raise ApiError(API_ERRORS['EMPTY_FORMDATA'])

    media = media_service.get_by_id(media_id)

    if media is None:
        raise ApiError(MEDIA_API_ERRORS['MEDIA_NOT_FOUND'])

    for file in files:
        media_file = request.files[file]
        data = media_file.read()
        extension = split_filename(media_file.filename).extension

        if not is_valid_jpg(data, extension):
            raise ApiError(API_ERRORS['INVALID_JPG'])

        try:
            saved_filename = image_service.save(data=data, extension=extension)
        except:
            raise ApiError(API_ERRORS['CANT_SAVE_FILE'])

        media_file_url = Static.IMAGES_URL + saved_filename
        formdata[file] = media_file_url

        filename = split_filename(getattr(media, file)).filename()
        try:
            image_service.delete(filename)
        except:
            pass

    if 'trailer' in formdata:
        name = split_filename(formdata['trailer']).name
        if video_service.find(name) is None:
            raise ApiError(VIDEO_API_ERRORS['VIDEO_NOT_FOUND'])

        formdata['trailer'] = concat_video_to_url(formdata['trailer'])

        if media.trailer:
            delete_videos_with_quality(media.trailer)

    dto = MediaUpdateDTO(**formdata)
    updated_media = media_service.update_media(id=media.id, update_media_dto=dto)

    return jsonify(updated_media._asdict())


@app.route('/media', methods=['DELETE'])
@jwt_required()
def delete_media():
    media_id = request.args.get('id')

    if media_id is None:
        raise ApiError(API_ERRORS['NO_IDENTITY_PROVIDED'])
    if not media_id.isdigit():
        raise ApiError(API_ERRORS['INVALID_ID'])

    media_id = int(media_id)

    media = media_service.get_by_id(media_id)
    if not media:
        raise ApiError(MEDIA_API_ERRORS['MEDIA_NOT_FOUND'])

    videos = media_video_service.get_media_videos(media.id)
    for video in videos:
        delete_videos_with_quality(video.source)

    media_service.delete_media(id=media_id)

    files = [media.thumbnail, media.preview]

    for file in files:
        filename = split_filename(file).filename()
        try:
            image_service.delete(filename)
        except:
            pass

    if media.trailer:
        delete_videos_with_quality(media.trailer)

    return jsonify(media._asdict())

