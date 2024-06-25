from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.app import app
from src.api.services.room import room_service
from src.api.services.user import user_service
from src.api.services.participant import participant_service
from src.api.services.image import image_service
from src.api.routes.room.schemas import (
    RoomSchema, CreateRoomSchema, UpdateRoomSchema, RoomFilesSchema
)
from src.api.routes.participant.schemas import ParticipantSchema
from src.usecase.room.dto import RoomDTO, RoomCreateDTO, RoomUpdateDTO
from src.usecase.dto import QueryParametersDTO
from src.api.error.shared_error import API_ERRORS
from src.api.routes.room.error import ROOM_API_ERRORS
from src.api.error.custom_error import ApiError

from src.configs.constants import Static

from pkg.query_params.select.parse import parse_select
from pkg.query_params.filter_by.parse import parse_filter_by
from pkg.query_params.expand.parse import parse_expand
from pkg.file.image.jpg_validate import is_valid_jpg
from pkg.file.filename import split_filename
from pkg.dict.keys import find_keys


FILES = ('cover',)
EXPAND_FIELDS = ('creator', 'participants')


@app.route('/room', methods=['POST'])
@jwt_required()
def create_room():
    RoomFilesSchema().validate(request.files)
    formdata = CreateRoomSchema().load(request.form)

    is_name_exists = room_service.is_field_exists('name', formdata['name'])
    if is_name_exists:
        raise ApiError(ROOM_API_ERRORS['ROOM_NAME_EXISTS'])

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

    user_id = int(get_jwt_identity())
    formdata['creatorId'] = user_id
    dto = RoomCreateDTO(**formdata)
    created_room = room_service.create_room(dto)

    return jsonify(created_room._asdict())


@app.route('/room', methods=['GET'])
def get_room_by_id_or_name():
    request_params = request.args

    room_id = request_params.get('id')
    room_name = request_params.get('name')

    if room_id is None and room_name is None:
        raise ApiError(API_ERRORS['NO_IDENTITY_PROVIDED'])

    expand = request_params.get('expand')
    try:
        expand = parse_expand(expand=expand, valid_fields=EXPAND_FIELDS)
    except:
        raise ApiError(API_ERRORS['INVALID_EXPAND'])

    select = request_params.get('select')
    room_fields = RoomDTO.__match_args__
    try:
        select = parse_select(select=select, valid_fields=room_fields)
    except:
        raise ApiError(API_ERRORS['INVALID_SELECT'])

    if room_id is not None:
        if not room_id.isdigit():
            raise ApiError(API_ERRORS['INVALID_ID'])
        room = room_service.get_room_by_id(room_id)
    else:
        room = room_service.get_room_by_name(room_name)

    if room is None:
        raise ApiError(ROOM_API_ERRORS['ROOM_NOT_FOUND'])

    serialize_room = RoomSchema(only=select).dump
    serialized_room = serialize_room(room)

    if not expand:
        return jsonify(serialized_room)

    if 'creator' in expand:
        creator = user_service.get_by_id(room.creatorId)
        serialized_room['creator'] = creator._asdict()

    if 'participants' in expand:
        serialize_participants = ParticipantSchema(many=True).dump
        participants = participant_service.get_room_participants(room.id)
        serialized_room['participants'] = serialize_participants(participants)

    return jsonify(serialized_room)


@app.route('/room/all', methods=['GET'])
def get_all_rooms():
    request_params = request.args

    select = request_params.get('select')
    filter_by = request_params.get('filter_by')

    expand = request_params.get('expand')
    try:
        expand = parse_expand(expand=expand, valid_fields=EXPAND_FIELDS)
    except:
        raise ApiError(API_ERRORS['INVALID_EXPAND'])

    room_fields = RoomDTO.__match_args__
    try:
        select = parse_select(select=select, valid_fields=room_fields)
    except:
        raise ApiError(API_ERRORS['INVALID_SELECT'])

    room_fields = RoomDTO.__annotations__
    try:
        filter_by = parse_filter_by(filter_query=filter_by, valid_fields=room_fields)
    except:
        raise ApiError(API_ERRORS['INVALID_FILTERS'])

    query_parameters_dto = QueryParametersDTO(filters=filter_by)
    rooms = room_service.get_rooms(query_parameters_dto=query_parameters_dto)

    if len(rooms) == 0:
        raise ApiError(ROOM_API_ERRORS['ROOMS_NOT_FOUND'])

    serialize_rooms = RoomSchema(only=select, many=True).dump
    serialized_rooms = serialize_rooms(rooms)

    if not expand:
        return jsonify(serialized_rooms)

    if 'creator' in expand:
        for i in range(len(rooms)):
            creator_id = rooms[i].creatorId
            creator = user_service.get_by_id(creator_id)
            serialized_rooms[i]['creator'] = creator._asdict()

    if 'participants' in expand:
        serialize_participants = ParticipantSchema(many=True).dump
        for i in range(len(rooms)):
            room_id = rooms[i].id
            participants = participant_service.get_room_participants(room_id)
            serialized_rooms[i]['participants'] = serialize_participants(participants)

    return jsonify(serialized_rooms)


@app.route('/room', methods=['PATCH'])
@jwt_required()
def update_room():
    room_id = request.args.get('id')

    if room_id is None:
        raise ApiError(API_ERRORS['NO_IDENTITY_PROVIDED'])

    if not room_id.isdigit():
        raise ApiError(API_ERRORS['INVALID_ID'])

    RoomFilesSchema().validate(request.files)
    formdata = UpdateRoomSchema().load(request.form)

    files = find_keys(request.files, FILES)

    if len(formdata) == 0 and not files:
        raise ApiError(API_ERRORS['EMPTY_FORMDATA'])

    room = room_service.get_room_by_id(room_id)
    user_id = int(get_jwt_identity())
    if room is None:
        raise ApiError(ROOM_API_ERRORS['ROOM_NOT_FOUND'])
    if room.creatorId != user_id:
        raise ApiError(ROOM_API_ERRORS['CREATOR_RIGHTS_REQUIRED'])

    for file in files:
        room_file = request.files[file]
        data = room_file.read()
        extension = split_filename(room_file.filename).extension

        if not is_valid_jpg(data, extension):
            raise ApiError(API_ERRORS['INVALID_JPG'])

        try:
            saved_filename = image_service.save(data=data, extension=extension)
        except:
            raise ApiError(API_ERRORS['CANT_SAVE_FILE'])

        room_file_url = Static.IMAGES_URL + saved_filename
        formdata[file] = room_file_url

        previous_filename = getattr(room, file)
        if previous_filename:
            filename = split_filename(previous_filename).filename()
            try:
                image_service.delete(filename)
            except:
                pass

    dto = RoomUpdateDTO(**formdata)
    updated_room = room_service.update_room(id=room_id, update_room_dto=dto)

    return jsonify(updated_room._asdict())


@app.route('/room', methods=['DELETE'])
@jwt_required()
def delete_room():
    room_id = request.args.get('id')
    user_id = int(get_jwt_identity())

    if room_id is None:
        raise ApiError(API_ERRORS['NO_IDENTITY_PROVIDED'])
    if not room_id.isdigit():
        raise ApiError(API_ERRORS['INVALID_ID'])

    room_id = int(room_id)
    room = room_service.get_room_by_id(room_id)
    if room is None:
        raise ApiError(ROOM_API_ERRORS['ROOM_NOT_FOUND'])
    if room.creatorId != user_id:
        raise ApiError(ROOM_API_ERRORS['CREATOR_RIGHTS_REQUIRED'])

    room_service.delete_room(room_id)

    if room.cover:
        filename = split_filename(room.cover).filename()
        try:
            image_service.delete(filename)
        except:
            pass

    return jsonify(room._asdict())
