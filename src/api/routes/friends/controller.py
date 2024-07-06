from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.app import app
from src.api.services.user import user_service
from src.api.error.shared_error import API_ERRORS
from src.api.routes.user.error import USER_API_ERRORS
from src.api.routes.friends.error import FRIENDS_API_ERRORS
from src.api.error.custom_error import ApiError
from src.api.routes.user.schemas import UserSchema, UpdateUserSchema


@app.route('/friends', methods=['POST'])
@jwt_required()
def add_friend():
    request_params = request.args

    user_id = get_jwt_identity()
    friend_id = int(request_params.get('friend_id'))

    if user_id == friend_id:
        raise ApiError(FRIENDS_API_ERRORS['CANNOT_ADD_YOURSELF'])

    is_user_exists = user_service.is_field_exists(name='id', value=friend_id)

    if not is_user_exists:
        raise ApiError(USER_API_ERRORS['USER_NOT_FOUND'])

    sent_request = user_service.has_request(
        requesting_user_id=user_id,
        receiving_user_id=friend_id
    )
    is_already_friends = user_service.is_already_friends(
        user_id=user_id,
        friend_id=friend_id
    )

    if sent_request or is_already_friends:
        raise ApiError(FRIENDS_API_ERRORS['ALREADY_REQUESTED'])

    received_request = user_service.has_request(
        requesting_user_id=friend_id,
        receiving_user_id=user_id
    )

    if received_request:
        added_friend = user_service.add_friend(
            requesting_user_id=user_id,
            receiving_user_id=friend_id,
            received_request=received_request
        )
        deleted_received_request = user_service.delete_friend_request(
            friend_id=friend_id,
            request=received_request

        )

    else:
        added_friend = user_service.send_friend_request(
            requesting_user_id=user_id,
            receiving_user_id=friend_id
        )

    return jsonify(added_friend._asdict())


@app.route('/friends', methods=['DELETE'])
@jwt_required()
def delete_friend():
    request_params = request.args

    user_id = get_jwt_identity()
    friend_id = int(request_params.get('friend_id'))

    is_friend_exists = user_service.is_field_exists(name='id', value=friend_id)

    if not is_friend_exists:
        raise ApiError(USER_API_ERRORS['USER_NOT_FOUND'])

    is_already_friends = user_service.is_already_friends(user_id=user_id, friend_id=friend_id)

    if not is_already_friends:
        raise ApiError(FRIENDS_API_ERRORS['FRIEND_NOT_FOUND'])

    deleted_friend = user_service.delete_friend(user_id=user_id, friend_id=friend_id)

    return jsonify(deleted_friend._asdict())


@app.route('/friends/delete', methods=['DELETE'])
@jwt_required()
def delete_sent_friend_request():
    request_params = request.args

    user_id = get_jwt_identity()
    friend_id = int(request_params.get('friend_id'))

    is_friend_exists = user_service.is_field_exists(name='id', value=friend_id)

    if not is_friend_exists:
        raise ApiError(USER_API_ERRORS['USER_NOT_FOUND'])

    sent_request = user_service.has_request(
        requesting_user_id=user_id,
        receiving_user_id=friend_id
    )

    if not sent_request:
        raise ApiError(FRIENDS_API_ERRORS['REQUEST_NOT_FOUND'])

    deleted_request_friend = user_service.delete_friend_request(
        friend_id=friend_id,
        request=sent_request
    )

    return jsonify(deleted_request_friend._asdict())


@app.route('/friends/reject', methods=['DELETE'])
@jwt_required()
def delete_received_friend_request():
    request_params = request.args

    user_id = get_jwt_identity()
    friend_id = int(request_params.get('friend_id'))

    is_friend_exists = user_service.is_field_exists(name='id', value=friend_id)

    if not is_friend_exists:
        raise ApiError(USER_API_ERRORS['USER_NOT_FOUND'])

    received_request = user_service.has_request(
        requesting_user_id=friend_id,
        receiving_user_id=user_id
    )

    if not received_request:
        raise ApiError(FRIENDS_API_ERRORS['REQUEST_NOT_FOUND'])

    deleted_request_friend = user_service.delete_friend_request(
        friend_id=friend_id,
        request=received_request
    )

    return jsonify(deleted_request_friend._asdict())


@app.route('/friends', methods=['GET'])
def get_user_friends():
    request_params = request.args

    user_id = request_params.get('id')

    if user_id is not None:
        if not user_id.isdigit():
            raise ApiError(API_ERRORS['INVALID_ID'])

        user = user_service.get_by_id(id=user_id)

        if user is None:
            raise ApiError(USER_API_ERRORS['USER_NOT_FOUND'])

    limit = request_params.get('limit')
    offset = request_params.get('offset')
    if limit or offset:
        try:
            limit = int(limit)
            offset = int(offset)
        except:
            raise ApiError(API_ERRORS['INVALID_PAGE_QUERY'])

    query_parameters_dto = QueryParametersDTO(limit=limit, offset=offset)
    users = user_service.get_friends(user_id=user_id, query_parameters_dto=query_parameters_dto)

    serialize_users = UserSchema(many=True).dump
    serialized_users = serialize_users(users)

    return jsonify(serialized_users)


@app.route('/friends/received', methods=['GET'])
@jwt_required()
def get_received_friend_requests():
    user_id = get_jwt_identity()

    users = user_service.get_received_friend_requests(user_id=user_id)

    serialize_users = UserSchema(many=True).dump
    serialized_users = serialize_users(users)

    return jsonify(serialized_users)


@app.route('/friends/sent', methods=['GET'])
@jwt_required()
def get_sent_friend_requests():
    user_id = get_jwt_identity()

    users = user_service.get_sent_friend_requests(user_id=user_id)

    serialize_users = UserSchema(many=True).dump
    serialized_users = serialize_users(users)

    return jsonify(serialized_users)
