from flask import request, jsonify, Response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    jwt_required, create_access_token,
    create_refresh_token, get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies, get_jwt
)

from src.app import app
from src.domain.user import User
from src.usecase.user.usecase import UserUsecase
from src.usecase.user.dto import UserRegisterDTO
from src.repository.user.sqla_repo import UserRepo
from src.repository.driver.postgres import postgresql_engine

from src.api.routes.user.error import API_ERRORS
from src.api.error.custom_error import ApiError
from src.api.routes.user.schemas import (
	RegisterSchema, 
	LoginSchema
)


def create_response_with_jwt(user: User) -> Response:
	user_dict = user.to_dict()
	del user_dict['passwordHash']

	user_id = user_dict['id']

	access_token = create_access_token(
		identity = user_id, 
		additional_claims = {'ADMIN': False}
	)

	refresh_token = create_refresh_token(
		identity = user_id, 
		additional_claims = {'ADMIN': False}
	)

	response = jsonify(user_dict)
	set_access_cookies(response, access_token)
	set_refresh_cookies(response, refresh_token)

	return response


@app.route('/user/signup', methods=['POST'])
def register():
	repo = UserRepo(postgresql_engine)
	service = UserUsecase(repo)
	
	request_json = request.json
	RegisterSchema().validate(request_json)

	username = request_json['username']
	email = request_json['email']

	if service.username_exists(username):
		raise ApiError(API_ERRORS['USERNAME_EXISTS'])

	if service.email_exists(email):
		raise ApiError(API_ERRORS['EMAIL_EXISTS'])


	request_json['passwordHash'] = generate_password_hash(request_json['password'])
	del request_json['password']

	registered_user = service.register(UserRegisterDTO(**request_json))
	response = create_response_with_jwt(registered_user)

	return response, 200


@app.route('/user/login', methods=['POST'])
def login():
	repo = UserRepo(postgresql_engine)
	service = UserUsecase(repo)
	
	request_json = request.json
	LoginSchema().validate(request_json)

	username = request_json['username']

	if not service.username_exists(username):
		raise ApiError(API_ERRORS['USERNAME_NO_EXIST'])

	found_user = service.get_by_username(username)

	if found_user.isBanned:
		raise ApiError(API_ERRORS['BANNED'])

	request_password = request_json['password']

	password_match = check_password_hash(
		found_user.passwordHash,
		request_password
	)

	if not password_match:
		raise ApiError(API_ERRORS['WRONG_PWD'])

	response = create_response_with_jwt(found_user)

	return response, 200


@app.route('/logout', methods=['POST'])
@jwt_required()
def logout_post():
	response = jsonify(logout=True)
	unset_jwt_cookies(response)
	
	return response


@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():

	claims = get_jwt()
	user_id = get_jwt_identity()
	adminRights = claims['ADMIN']

	access_token = create_access_token(
		identity=user_id, 
		additional_claims={'ADMIN': adminRights}
	)

	response = jsonify(refresh=True)
	set_access_cookies(response, access_token)

	return response


@app.route('/user', methods=['DELETE'])
@jwt_required()
def delete_user():
	repo = UserRepo(postgresql_engine)
	service = UserUsecase(repo)

	user_id = get_jwt_identity()

	deleted_user = service.delete_user(id=user_id)

	response = jsonify(deleted_user.to_dict())
	unset_jwt_cookies(response)

	return response