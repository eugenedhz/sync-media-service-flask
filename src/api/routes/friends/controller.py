from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.app import app
from src.api.services.user import user_service
from src.api.error.shared_error import API_ERRORS
from src.api.routes.user.error import USER_API_ERRORS
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

    users = user_service.get_friends(id=user_id)

    serialize_users = UserSchema(many=True).dump
    serialized_users = serialize_users(users)

    return jsonify(serialized_users)


@app.route('/friends', methods=['POST'])
@jwt_required()
def add_friend():
    request_params = request.args

    user_id = get_jwt_identity()
    friend_id = request_params.get('friend_id')

    is_user_exists = user_service.is_field_exists(name='id', value=int(friend_id))

    if not is_user_exists:
        raise ApiError(USER_API_ERRORS['USER_NOT_FOUND'])

    added_friend = user_service.add_friend(id=user_id, friend_id=friend_id)

    serialize_user = UserSchema().dump
    serialized_user = serialize_user(added_friend)

    return jsonify(serialized_user)


@app.route('/friends', methods=['DELETE'])
@jwt_required()
def delete_friend():
    request_params = request.args

    user_id = get_jwt_identity()
    friend_id = request_params.get('friend_id')

    is_friend_exists = user_service.is_field_exists(name='id', value=int(friend_id))

    if not is_friend_exists:
        raise ApiError(USER_API_ERRORS['USER_NOT_FOUND'])

    deleted_friend = user_service.delete_friend(id=user_id, friend_id=friend_id)

    serialize_user = UserSchema().dump
    serialized_user = serialize_user(deleted_friend)

    return jsonify(serialized_user)
