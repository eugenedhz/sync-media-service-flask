from flask import request, jsonify
from flask_jwt_extended import jwt_required

from src.app import app
from src.api.services.genre import genre_service
from src.api.services.media import media_service
from src.usecase.dto import QueryParametersDTO
from src.usecase.genre.dto import (
    GenreDTO, GenreCreateDTO, GenreCreateDTO, GenreUpdateDTO
)
from src.api.routes.genre.schemas import (
    GenreSchema, UpdateGenreSchema, CreateGenreSchema, GenreAddOrDeleteFromMediaSchema
)
from src.api.error.shared_error import API_ERRORS
from src.api.routes.genre.error import GENRE_API_ERRORS
from src.api.routes.media.error import MEDIA_API_ERRORS
from src.api.error.custom_error import ApiError
from src.configs.constants import Role
from src.api.helpers.jwt import role_required

from pkg.query_params.select.parse import parse_select
from pkg.query_params.filter_by.parse import parse_filter_by
 

@app.route('/genre', methods=['POST'])
@jwt_required()
@role_required(Role.ADMIN)
def genre_create():
    CreateGenreSchema().validate(request.json)

    is_slug_exists = genre_service.is_field_exists('slug', request.json['slug'])
    if is_slug_exists:
        raise ApiError(GENRE_API_ERRORS['SLUG_EXISTS'])

    dto = GenreCreateDTO(**request.json)
    genre = genre_service.create_genre(dto)

    return jsonify(genre._asdict())


@app.route('/genre', methods=['GET'])
def get_genre_by_slug_or_id():
    request_params = request.args

    genre_slug = request_params.get('slug')
    genre_id = request_params.get('id')

    if (genre_slug is None) and (genre_id is None):
        raise ApiError(API_ERRORS['NO_IDENTITY_PROVIDED'])
    
    select = request_params.get('select')
    genre_fields = GenreDTO.__match_args__
    try:
        select = parse_select(select=select, valid_fields=genre_fields)
    except:
        raise ApiError(API_ERRORS['INVALID_SELECT'])
    
    if genre_id:
        genre = genre_service.get_genre_by_id(id=genre_id)
    else:
        genre = genre_service.get_genre_by_slug(slug=genre_slug)

    if genre is None:
        raise ApiError(GENRE_API_ERRORS['GENRE_NOT_FOUND'])
    
    serialize_genre = GenreSchema(only=select).dump
    serialized_genre = serialize_genre(genre)

    return jsonify(serialized_genre)


@app.route('/genre/all', methods=['GET'])
def get_all_genres():
    request_params = request.args

    select = request_params.get('select')
    filter_by = request_params.get('filter_by')

    genre_fields = GenreDTO.__match_args__
    try:
        select = parse_select(select=select, valid_fields=genre_fields)
    except:
        raise ApiError(API_ERRORS['INVALID_SELECT'])
    
    genre_fields = GenreDTO.__annotations__
    try:
        filter_by = parse_filter_by(filter_query=filter_by, valid_fields=genre_fields)
    except:
        raise ApiError(API_ERRORS['INVALID_FILTERS'])
    
    query_parameters_dto = QueryParametersDTO(filters=filter_by)
    genres = genre_service.get_genres(query_parameters_dto=query_parameters_dto)

    if len(genres) == 0:
        raise ApiError(GENRE_API_ERRORS['GENRES_NOT_FOUND'])
    
    serialize_genres = GenreSchema(only=select, many=True).dump
    serialized_genres = serialize_genres(genres)

    return jsonify(serialized_genres)


@app.route('/media/genre', methods=['GET'])
def get_media_genres():
    media_id = request.args.get('mediaId')

    if media_id is None:
        raise ApiError(API_ERRORS['NO_IDENTITY_PROVIDED'])

    if not media_id.isdigit():
        raise ApiError(API_ERRORS['INVALID_ID'])

    is_media_exists = media_service.is_field_exists('id', media_id)
    if not is_media_exists:
        raise ApiError(MEDIA_API_ERRORS['MEDIA_NOT_FOUND'])

    genre_fields = GenreDTO.__match_args__
    select = request.args.get('select')
    try:
        select = parse_select(select=select, valid_fields=genre_fields)
    except Exception as e:
        raise ApiError(API_ERRORS['INVALID_SELECT'])
    
    genres = genre_service.get_media_genres(media_id)

    if len(genres) == 0:
        raise ApiError(GENRE_API_ERRORS['MEDIA_GENRES_NOT_FOUND'])
    
    serialize_genres = GenreSchema(only=select, many=True).dump
    serialized_genres = serialize_genres(genres)

    return jsonify(serialized_genres)


@app.route('/media/genre', methods=['POST'])
@jwt_required()
@role_required(Role.ADMIN)
def add_genre_to_media():
    GenreAddOrDeleteFromMediaSchema().validate(request.json)
    json = request.json

    is_media_exists = media_service.is_field_exists('id', json['mediaId'])
    if not is_media_exists:
        raise ApiError(MEDIA_API_ERRORS['MEDIA_NOT_FOUND'])

    is_genre_exists = genre_service.is_field_exists('id', json['genreId'])
    if not is_genre_exists:
        raise ApiError(GENRE_API_ERRORS['GENRE_NOT_FOUND'])

    is_media_genre_exist = genre_service.is_media_genre_exist(
        media_id=json['mediaId'],
        genre_id=json['genreId']
    )

    if is_media_genre_exist:
        raise ApiError(GENRE_API_ERRORS['MEDIA_GENRE_EXISTS'])

    genre = genre_service.add_genre_to_media(media_id=json['mediaId'], genre_id=json['genreId'])

    return jsonify(genre._asdict())


@app.route('/media/genre', methods=['DELETE'])
@jwt_required()
@role_required(Role.ADMIN)
def delete_genre_from_media():
    GenreAddOrDeleteFromMediaSchema().validate(request.json)
    json = request.json

    is_media_exists = media_service.is_field_exists('id', json['mediaId'])
    if not is_media_exists:
        raise ApiError(MEDIA_API_ERRORS['MEDIA_NOT_FOUND'])

    is_genre_exists = genre_service.is_field_exists('id', json['genreId'])
    if not is_genre_exists:
        raise ApiError(GENRE_API_ERRORS['GENRE_NOT_FOUND'])

    is_media_genre_exist = genre_service.is_media_genre_exist(
        media_id = json['mediaId'],
        genre_id = json['genreId']
    )

    if not is_media_genre_exist:
        raise ApiError(GENRE_API_ERRORS['MEDIA_GENRE_NOT_FOUND'])

    genre = genre_service.delete_genre_from_media(media_id=json['mediaId'], genre_id=json['genreId'])

    return jsonify(genre._asdict())


@app.route('/genre', methods=['PATCH'])
@jwt_required()
@role_required(Role.ADMIN)
def update_genre():
    genre_id = request.args.get('id')

    if genre_id is None:
        raise ApiError(API_ERRORS['NO_IDENTITY_PROVIDED'])

    if not genre_id.isdigit():
        raise ApiError(API_ERRORS['INVALID_ID'])

    UpdateGenreSchema().validate(request.json)

    is_genre_exist = genre_service.is_field_exists(name="id", value=genre_id)
    if not is_genre_exist:
        raise ApiError(GENRE_API_ERRORS['GENRE_NOT_FOUND'])

    if 'slug' in request.json:
        is_slug_exists = genre_service.is_field_exists('slug', request.json['slug'])
        if is_slug_exists:
            raise ApiError(GENRE_API_ERRORS['SLUG_EXISTS'])

    dto = GenreUpdateDTO(**request.json)
    updated_genre = genre_service.update_genre(id=genre_id, update_genre_dto=dto)

    return jsonify(updated_genre._asdict())


@app.route('/genre', methods=['DELETE'])
@jwt_required()
@role_required(Role.ADMIN)
def delete_genre():
    genre_id = request.args.get('id')

    if genre_id is None:
        raise ApiError(API_ERRORS['NO_IDENTITY_PROVIDED'])

    if not genre_id.isdigit():
        raise ApiError(API_ERRORS['INVALID_ID'])
    
    if not genre_service.is_field_exists(name="id", value=genre_id):
        raise ApiError(GENRE_API_ERRORS['GENRE_NOT_FOUND'])
    
    deleted_genre = genre_service.delete_genre(id=genre_id)

    return jsonify(deleted_genre._asdict())