from flask import request, jsonify
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity, set_access_cookies,
    unset_jwt_cookies, get_jwt
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
from src.configs.constants import Role, Static

from pkg.query_params.select.parse import parse_select
from pkg.query_params.filter_by.parse import parse_filter_by
from pkg.query_params.ids.validate import is_valid_ids
from pkg.file.image.jpg_validate import is_valid_jpg
from pkg.file.filename import get_filename, get_extension


@app.route('/media', methods=['POST'])
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
#
#
# @app.route('/user/all', methods=['GET'])
# def get_all_users():
#     request_params = request.args
#
#     user_ids = request_params.get('ids')
#
#     if user_ids is not None:
#         user_ids = tuple(user_ids.split(','))
#
#         if not is_valid_ids(ids=user_ids):
#             raise ApiError(API_ERRORS['INVALID_ID'])
#
#     select = request_params.get('select')
#     filter_by = request_params.get('filter_by')
#
#     user_fields = UserDTO.__match_args__
#     try:
#         select = parse_select(select=select, valid_fields=user_fields)
#     except:
#         raise ApiError(API_ERRORS['INVALID_SELECT'])
#
#     # .__annotations__ возвращает словарь {поле: тип поля}
#     user_fields = UserDTO.__annotations__
#     try:
#         filter_by = parse_filter_by(filter_query=filter_by, valid_fields=user_fields)
#     except:
#         raise ApiError(API_ERRORS['INVALID_FILTERS'])
#
#     query_parameters = QueryParametersDTO(filters=filter_by)
#     users = user_service.get_users(ids=user_ids, query_parameters=query_parameters)
#
#     if len(users) == 0:
#         raise ApiError(USER_API_ERRORS['USERS_NOT_FOUND'])
#
#     serialize_users = UserSchema(only=select, many=True).dump
#     serialized_users = serialize_users(users)
#
#     return jsonify(serialized_users)
#
#
@app.route('/media', methods=['PATCH'])
@jwt_required()
def update_media():
    media_id = get_jwt_identity()

    formdata = request.form.to_dict(flat=True)
    parsed_formdata = UpdateMediaSchema().load(formdata)

    if len(parsed_formdata) == 0 and 'preview' not in request.files and 'thumbnail' not in request.files:
        raise ApiError(API_ERRORS['EMPTY_FORMDATA'])

    if 'name' in parsed_formdata:
        name = parsed_formdata['name']

        name_exists = media_service.field_exists(name='name', value=name)
        if name_exists:
            raise ApiError(MEDIA_API_ERRORS['NAME_EXISTS'])

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

        media = media_service.get_by_id(media_id)
        thumbnail = media.thumbnail

        if thumbnail is not None:
            filename = get_filename(thumbnail)
            try:
                image_service.delete(filename)
            except:
                pass

        thumbnail_url = Static.IMAGES_URL + saved_filename
        parsed_formdata['thumbnail'] = thumbnail_url

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

        media = media_service.get_by_id(media_id)
        preview = media.preview

        if preview is not None:
            filename = get_filename(preview)
            try:
                image_service.delete(filename)
            except:
                pass

        preview_url = Static.IMAGES_URL + saved_filename
        parsed_formdata['preview'] = preview_url

    dto = MediaUpdateDTO(**parsed_formdata)
    updated_media = media_service.update_media(id=media_id, update_media_dto=dto)

    return jsonify(updated_media._asdict())


#
#
# @app.route('/user', methods=['DELETE'])
# @jwt_required()
# def delete_user():
#     user_id = request.args.get('id')
#
#     if user_id is None:
#         raise ApiError(API_ERRORS['NO_IDENTITY_PROVIDED'])
#     if not user_id.isdigit():
#         raise ApiError(API_ERRORS['INVALID_ID'])
#
#     user_id = int(user_id)
#     jwt_user_id = int(get_jwt_identity())
#
#     if user_id != jwt_user_id:
#         claims = get_jwt()
#         admin_rights = claims[Role.ADMIN]
#
#         if not admin_rights:
#             raise ApiError(API_ERRORS['ADMIN_RIGHTS_REQUIRED'])
#
#     user_exists = user_service.field_exists(name='id', value=user_id)
#     if not user_exists:
#         raise ApiError(USER_API_ERRORS['USER_NOT_FOUND'])
#
#     deleted_user = user_service.delete_user(id=user_id)
#     avatar = deleted_user.avatar
#
#     if avatar is not None:
#         filename = get_filename(avatar)
#         try:
#             image_service.delete(filename)
#         except:
#             pass
#
#     return deleted_user._asdict()
