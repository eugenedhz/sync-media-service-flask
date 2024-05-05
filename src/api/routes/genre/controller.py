from flask import request, jsonify
from flask_jwt_extended import jwt_required

from src.app import app
from src.api.services.genre import genre_service
from src.usecase.dto import QueryParametersDTO
from src.usecase.genre.dto import GenreDTO
from src.api.error.shared_error import API_ERRORS
from src.api.routes.genre.error import GENRE_API_ERRORS
from src.api.error.custom_error import ApiError
from src.api.routes.genre.schemas import GenreSchema

from pkg.query_params.select.parse import parse_select
from pkg.query_params.filter_by.parse import parse_filter_by
from pkg.dict.keys import find_keys

@app.route('/genre', methods=['POST'])
@jwt_required()
def genre_create():
    request_json = request.json
    GenreSchema().validate(request_json)
    formdata = request.form.to_dict(flat=True)
    parsed_formdata = GenreSchema().load(formdata)
    dto = GenreDTO(**parsed_formdata)
    create_genre = genre_service.create_genre(dto)

    return create_genre._asdict()

@app.route('/media', methods=['GET'])
def get_genre_by_slug():
    request_params = request.args
    genre_slug = request_params.get("slug")

    if genre_slug is None:
        raise ApiError(API_ERRORS['NO_IDENTITY_PROVIDED'])
    
    select = request_params.get('select')
    genre_fields = GenreDTO.__match_args__
    try:
        select = parse_select(select=select, valid_fields=genre_fields)
    except:
        raise ApiError(API_ERRORS['INVALID_SELECT'])
    
    genre = genre_service.get_by_slug(slug=genre_slug)

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
    
    # .__annotations__ возвращает словарь {поле: тип поля}
    genre_fields = GenreDTO.__annotations__
    try:
        filter_by = parse_filter_by(filter_query=filter_by, valid_fields=genre_fields)
    except:
        raise ApiError(API_ERRORS['INVALID_FILTERS'])
    
    query_parameters_dto = QueryParametersDTO(filters=filter_by)
    genres = genre_service.get_genres(query_parameters_dto=query_parameters_dto)

    if len(genres) == 0:
        raise ApiError(GENRE_API_ERRORS['GENRE_NOT_FOUND'])
    
    serialize_genres = GenreSchema(only=select, many=True).dump
    serialized_genres = serialize_genres(genres)

    return jsonify(serialized_genres)


@app.route('/genre', methods=['PATCH'])
@jwt_required()
def update_genre():
    genre_slug = request.args.get('slug')

    if genre_slug is None:
        raise ApiError(API_ERRORS['INVALID_REQUEST'])
    
    formdata = request.form.to_dict(flat=True)
    parsed_formdata = GenreSchema().load(formdata)

    if len(parsed_formdata) == 0:
        raise ApiError(API_ERRORS['EMPTY_FORMDATA'])
    
    genre = genre_service.get_by_slug(genre_slug)

    if genre is None:
        raise ApiError(GENRE_API_ERRORS['GENRE_NOT_FOUND'])
    
    dto = GenreDTO(**parsed_formdata)
    updated_genre = genre_service.update_genre(slug=genre_slug, update_genre_dto=dto)

    return jsonify(updated_genre._asdict())


@app.route('/genre', methods=['DELETE'])
@jwt_required()
def delete_genre():
    genre_slug = request.args.get('slug')

    if genre_slug is None:
        raise ApiError(API_ERRORS['INVALID_REQUEST'])
    
    is_genre_exists = genre_service.is_field_exists(name="slug", value=genre_slug)
    if not is_genre_exists:
        raise ApiError(GENRE_API_ERRORS['GENRE_NOT_FOUND'])
    
    deleted_genre = genre_service.delete_genre(slug=genre_slug)

    return deleted_genre._asdict()