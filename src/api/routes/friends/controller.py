from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.app import app
from src.api.services.user import user_service
from src.api.error.shared_error import API_ERRORS
from src.api.routes.user.error import USER_API_ERRORS
from src.api.routes.friends.error import FRIENDS_API_ERRORS
from src.api.error.custom_error import ApiError
from src.api.routes.user.schemas import UserSchema, UpdateUserSchema


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

    users = user_service.get_friends(user_id=user_id)

    serialize_users = UserSchema(many=True).dump
    serialized_users = serialize_users(users)

    return jsonify(serialized_users)


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

    already_requested_ids = user_service.get_already_requested_users_ids(user_id=user_id)

    if friend_id in already_requested_ids:
        raise ApiError(FRIENDS_API_ERRORS['ALREADY_REQUESTED'])

    added_friend = user_service.add_friend(requesting_user_id=user_id, receiving_user_id=friend_id)

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

    user_friends_ids = user_service.get_friends_ids(user_id=user_id)

    if friend_id not in user_friends_ids:
        raise ApiError(FRIENDS_API_ERRORS['FRIEND_NOT_FOUND'])

    deleted_friend = user_service.delete_friend(user_id=user_id, friend_id=friend_id)

    return jsonify(deleted_friend._asdict())


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


@app.route('/friends/delete', methods=['DELETE'])
@jwt_required()
def delete_sent_friend_request():
    request_params = request.args

    user_id = get_jwt_identity()
    friend_id = int(request_params.get('friend_id'))

    is_friend_exists = user_service.is_field_exists(name='id', value=friend_id)

    if not is_friend_exists:
        raise ApiError(USER_API_ERRORS['USER_NOT_FOUND'])

    sent_request_ids = user_service.get_sent_requests_friends_ids(user_id=user_id)

    if friend_id not in sent_request_ids:
        raise ApiError(FRIENDS_API_ERRORS['REQUEST_NOT_FOUND'])

    deleted_request_friend = user_service.delete_sent_friend_request(requesting_user_id=user_id, receiving_user_id=friend_id)

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

    received_requests_ids = user_service.get_received_requests_friends_ids(user_id=user_id)

    if friend_id not in received_requests_ids:
        raise ApiError(FRIENDS_API_ERRORS['REQUEST_NOT_FOUND'])

    deleted_request_friend = user_service.delete_received_friend_request(user_id=user_id, requesting_user_id=friend_id)

    return jsonify(deleted_request_friend._asdict())
