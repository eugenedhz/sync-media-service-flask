from flask import request, jsonify
from flask_jwt_extended import (
    jwt_required
)

from src.app import app
from src.api.services.media import media_service
from src.api.services.image import image_service
from src.usecase.dto import QueryParametersDTO
from src.usecase.media.dto import MediaDTO, MediaUpdateDTO, MediaCreateDTO
from src.api.error.shared_error import API_ERRORS
from src.api.routes.media.error import MEDIA_API_ERRORS
from src.api.error.custom_error import ApiError
from src.api.routes.media.schemas import MediaSchema, UpdateMediaSchema, CreateMediaSchema
from src.configs.constants import Static

from pkg.query_params.select.parse import parse_select
from pkg.query_params.filter_by.parse import parse_filter_by
from pkg.query_params.ids.validate import is_valid_ids
from pkg.file.image.jpg_validate import is_valid_jpg
from pkg.file.filename import get_filename, get_extension


@app.route('/media', methods=['POST'])
@jwt_required()
def media_create():
    
    formdata = request.form.to_dict(flat=True)
    parsed_formdata = UpdateMediaSchema().load(formdata)

    name = parsed_formdata['name']

    if 'thumbnail' in request.files:
        image = request.files['thumbnail']
        data = image.read()
        extension = get_extension(image.filename)

        if not is_valid_jpg(data, extension):
            raise ApiError(API_ERRORS['INVALID_JPG'])

        try:
            saved_filename = image_service.save(data=data, extension=extension)
        except:
            raise ApiError(API_ERRORS['CANT_SAVE_FILE'])

        thumbnail_url = Static.IMAGES_URL + saved_filename
        parsed_formdata['thumbnail'] = thumbnail_url
    else:
        raise ApiError(MEDIA_API_ERRORS['THUMBNAIL_NOT_PROVIDED'])
        
    if 'preview' in request.files:
        image = request.files['preview']
        data = image.read()
        extension = get_extension(image.filename)

        if not is_valid_jpg(data, extension):
            raise ApiError(API_ERRORS['INVALID_JPG'])

        try:
            saved_filename = image_service.save(data=data, extension=extension)
        except:
            raise ApiError(API_ERRORS['CANT_SAVE_FILE'])

        preview_url = Static.IMAGES_URL + saved_filename
        parsed_formdata['preview'] = preview_url
    else:
        raise ApiError(MEDIA_API_ERRORS['PREVIEW_NOT_PROVIDED'])

    media_exists = media_service.field_exists(name='name', value=name)
    if media_exists:
        raise ApiError(MEDIA_API_ERRORS['MEDIA_EXISTS'])

    dto = MediaCreateDTO(**parsed_formdata)
    created_media = media_service.create_media(dto)

    response = created_media._asdict()

    return response


@app.route('/media', methods=['GET'])
def get_media_by_name_or_id():
    request_params = request.args

    name = request_params.get('name')
    media_id = request_params.get('id')

    if (name is None) and (media_id is None):
        raise ApiError(API_ERRORS['NO_IDENTITY_PROVIDED'])

    select = request_params.get('select')
    media_fields = MediaDTO.__match_args__
    try:
        select = parse_select(select=select, valid_fields=media_fields)
    except:
        raise ApiError(API_ERRORS['INVALID_SELECT'])

    if media_id is not None:
        if not media_id.isdigit():
            raise ApiError(API_ERRORS['INVALID_ID'])

        media = media_service.get_by_id(id=media_id)

        if media is None:
            raise ApiError(MEDIA_API_ERRORS['MEDIA_NOT_FOUND'])

    else:
        media = media_service.get_by_name(name=name)

        if media is None:
            raise ApiError(MEDIA_API_ERRORS['MEDIA_NOT_FOUND'])

    serialize_media = MediaSchema(only=select).dump
    serialized_media = serialize_media(media)

    return jsonify(serialized_media)


@app.route('/media/all', methods=['GET'])
def get_all_medias():
    request_params = request.args

    media_ids = request_params.get('ids')

    if media_ids is not None:
        media_ids = tuple(media_ids.split(','))

        if not is_valid_ids(ids=media_ids):
            raise ApiError(API_ERRORS['INVALID_ID'])

    select = request_params.get('select')
    filter_by = request_params.get('filter_by')

    media_fields = MediaDTO.__match_args__
    try:
        select = parse_select(select=select, valid_fields=media_fields)
    except:
        raise ApiError(API_ERRORS['INVALID_SELECT'])

    # .__annotations__ возвращает словарь {поле: тип поля}
    media_fields = MediaDTO.__annotations__
    try:
        filter_by = parse_filter_by(filter_query=filter_by, valid_fields=media_fields)
    except:
        raise ApiError(API_ERRORS['INVALID_FILTERS'])

    query_parameters = QueryParametersDTO(filters=filter_by)
    medias = media_service.get_medias(ids=media_ids, query_parameters=query_parameters)

    if len(medias) == 0:
        raise ApiError(MEDIA_API_ERRORS['MEDIA_NOT_FOUND'])

    serialize_medias = MediaSchema(only=select, many=True).dump
    serialized_medias = serialize_medias(medias)

    return jsonify(serialized_medias)


@app.route('/media', methods=['PATCH'])
@jwt_required()
def update_media():

    formdata = request.form.to_dict(flat=True)
    parsed_formdata = UpdateMediaSchema().load(formdata)
    media_id = parsed_formdata['id']
    media = media_service.get_by_id(media_id)

    if len(parsed_formdata) == 0 and 'preview' not in request.files and 'thumbnail' not in request.files:
        raise ApiError(API_ERRORS['EMPTY_FORMDATA'])

    if 'name' in parsed_formdata:
        if parsed_formdata['name'] != "":
            name = parsed_formdata['name']

            name_exists = media_service.field_exists(name='name', value=name)
            if name_exists:
                raise ApiError(MEDIA_API_ERRORS['MEDIA_NAME_EXISTS'])
        else:
            parsed_formdata['name'] = media.name

    if 'thumbnail' in request.files:
        thumbnail = request.files['thumbnail']
        data = thumbnail.read()
        extension = get_extension(thumbnail.filename)

        if not is_valid_jpg(data, extension):
            raise ApiError(API_ERRORS['INVALID_JPG'])

        try:
            saved_filename = image_service.save(data=data, extension=extension)
        except:
            raise ApiError(API_ERRORS['CANT_SAVE_FILE'])

        thumbnail = media.thumbnail

        if parsed_formdata['thumbnail'] != "":
            if thumbnail is not None:
                filename = get_filename(thumbnail)
                try:
                    image_service.delete(filename)
                except:
                    pass

            thumbnail_url = Static.IMAGES_URL + saved_filename
            parsed_formdata['thumbnail'] = thumbnail_url
    else:
        parsed_formdata['thumbnail'] = media.thumbnail

    if 'preview' in request.files:
        preview = request.files['preview']
        data = preview.read()
        extension = get_extension(preview.filename)

        if not is_valid_jpg(data, extension):
            raise ApiError(API_ERRORS['INVALID_JPG'])

        try:
            saved_filename = image_service.save(data=data, extension=extension)
        except:
            raise ApiError(API_ERRORS['CANT_SAVE_FILE'])

        preview = media.preview

        if parsed_formdata['preview'] != "":
            if preview is not None:
                filename = get_filename(preview)
                try:
                    image_service.delete(filename)
                except:
                    pass

            preview_url = Static.IMAGES_URL + saved_filename
            parsed_formdata['preview'] = preview_url
    else:
        parsed_formdata['preview'] = media.preview

    dto = MediaUpdateDTO(**parsed_formdata)
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

    media_exists = media_service.field_exists(name='id', value=media_id)
    if not media_exists:
        raise ApiError(MEDIA_API_ERRORS['MEDIA_NOT_FOUND'])

    deleted_media = media_service.delete_media(id=media_id)
    thumbnail = deleted_media.thumbnail

    if thumbnail is not None:
        filename = get_filename(thumbnail)
        try:
            image_service.delete(filename)
        except:
            pass

    preview = deleted_media.preview

    if preview is not None:
        filename = get_filename(preview)
        try:
            image_service.delete(filename)
        except:
            pass

    return deleted_media._asdict()
