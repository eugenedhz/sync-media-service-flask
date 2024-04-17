from flask import request, jsonify
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity, set_access_cookies,
    unset_jwt_cookies, get_jwt
)

from src.app import app
from src.configs.constants import Role
from src.api.services.user import user_service
from src.usecase.user.dto import UserCreateDTO, UserCheckPasswordDTO
from src.api.routes.auth.responses import create_response_with_jwt, Claims
from src.api.error.shared_error import API_ERRORS
from src.api.routes.auth.error import AUTH_API_ERRORS
from src.api.routes.user.error import USER_API_ERRORS
from src.api.error.custom_error import ApiError
from src.api.routes.auth.schemas import RegisterSchema, LoginSchema


@app.route('/auth/signup', methods=['POST'])
def register():
	request_json = request.json
	RegisterSchema().validate(request_json)

	username = request_json['username']
	email = request_json['email']

	is_username_exists = user_service.is_field_exists(name='username', value=username)
	if is_username_exists:
		raise ApiError(AUTH_API_ERRORS['USERNAME_EXISTS'])

	is_email_exists = user_service.is_field_exists(name='email', value=email)
	if is_email_exists:
		raise ApiError(AUTH_API_ERRORS['EMAIL_EXISTS'])

	dto = UserCreateDTO(**request_json)
	user = user_service.create_user(dto)

	claims = Claims(role=Role.USER)
	response = create_response_with_jwt(
		user = user._asdict(),
		claims = claims
	)

	return response


@app.route('/auth/login', methods=['POST'])
def login():
	request_json = request.json
	LoginSchema().validate(request_json)

	username = request_json['username']
	password = request_json['password']
	user = user_service.get_by_username(username)

	if user is None:
		raise ApiError(AUTH_API_ERRORS['USERNAME_NOT_FOUND'])

	if user.isBanned:
		raise ApiError(AUTH_API_ERRORS['BANNED'])
	
	dto = UserCheckPasswordDTO(
		username = username,
		password = password
	)
	password_match = user_service.check_user_password(dto)

	if not password_match:
		raise ApiError(AUTH_API_ERRORS['WRONG_PWD'])

	claims = Claims(role=Role.USER)
	response = create_response_with_jwt(
		user = user._asdict(),
		claims = claims
	)

	return response


@app.route('/auth/logout', methods=['POST'])
@jwt_required()
def logout_post():
	response = jsonify(logout=True)
	unset_jwt_cookies(response)
	
	return response


@app.route('/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
	claims = get_jwt()
	user_id = get_jwt_identity()

	user = user_service.get_by_id(user_id)

	if user is None:
		raise ApiError(USER_API_ERRORS['USER_NOT_FOUND'])

	response = create_response_with_jwt(
		user = user._asdict(), 
		claims = claims
	)

	return response