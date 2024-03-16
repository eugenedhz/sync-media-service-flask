from flask import request, jsonify
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity, set_access_cookies,
    unset_jwt_cookies, get_jwt
)

from src.app import app
from src.domain.user import User
from src.usecase.user.usecase import UserUsecase
from src.usecase.user.dto import UserRegisterDTO, UserDTO, LoginDTO, UserUpdateDTO
from src.repository.user.sqla_repo import UserRepo
from src.repository.driver.postgres import postgresql_engine
from src.api.routes.user.responses import create_response_with_jwt
from src.api.error.shared_error import API_ERRORS
from src.api.routes.user.error import USER_API_ERRORS
from src.api.error.custom_error import ApiError
from src.api.routes.user.schemas import (
	RegisterSchema, LoginSchema, UserSchema, UpdateUserSchema
)

from pkg.query_params.select.parse import parse_select
from pkg.query_params.filter_by.parse import parse_filter_by
from pkg.query_params.ids.validate import is_valid_ids
from pkg.formdata.parse import parse_formdata
from pkg.image.jpg_validate import is_valid_jpg


@app.route('/user/signup', methods=['POST'])
def register():
	repo = UserRepo(postgresql_engine)
	user_service = UserUsecase(repo)
	
	request_json = request.json
	RegisterSchema().validate(request_json)

	username = request_json['username']
	email = request_json['email']

	found_user = user_service.get_by_username(username=username)
	if found_user is not None:
		raise ApiError(USER_API_ERRORS['USERNAME_EXISTS'])

	if user_service.email_exists(email):
		raise ApiError(USER_API_ERRORS['EMAIL_EXISTS'])

	register_dto = UserRegisterDTO(**request_json)
	registered_user = user_service.register(register_dto)

	response = create_response_with_jwt(registered_user._asdict())

	return response, 200


@app.route('/user/login', methods=['POST'])
def login():
	repo = UserRepo(postgresql_engine)
	user_service = UserUsecase(repo)
	
	request_json = request.json
	LoginSchema().validate(request_json)

	request_username = request_json['username']
	request_password = request_json['password']
	found_user = user_service.get_by_username(request_username)

	if found_user is None:
		raise ApiError(USER_API_ERRORS['USERNAME_NO_EXIST'])

	if found_user.isBanned:
		raise ApiError(USER_API_ERRORS['BANNED'])
	
	login_dto = LoginDTO(
		username = request_username,
		password = request_password
	)
	password_match = user_service.check_user_password(login_dto)

	if not password_match:
		raise ApiError(USER_API_ERRORS['WRONG_PWD'])

	response = create_response_with_jwt(found_user._asdict())

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
	admin_rights = claims['ADMIN']

	access_token = create_access_token(
		identity=user_id, 
		additional_claims={'ADMIN': admin_rights}
	)

	response = jsonify(refresh=True)
	set_access_cookies(response, access_token)

	return response


@app.route('/user', methods=['GET'])
def get_user_by_username_or_id():
	repo = UserRepo(postgresql_engine)
	user_service = UserUsecase(repo)

	request_params = request.args

	request_username = request_params.get('username')
	request_user_id = request_params.get('id')

	request_select_fields = request_params.get('select')
	valid_select_fields = UserDTO.__match_args__
	parsed_select_fields = parse_select(
		select_fields = request_select_fields,
		valid_fields = valid_select_fields
	)

	if (request_username is None) and (request_user_id is None):
		raise ApiError(API_ERRORS['NO_IDENTITY_PROVIDED'])

	if request_user_id is not None:
		if not request_user_id.isdigit():
			raise ApiError(API_ERRORS['INVALID_ID'])

		user = user_service.get_by_id(id=request_user_id)

		if user is None:
			raise ApiError(API_ERRORS['USERNAME_NO_EXIST'])

	else:
		user = user_service.get_by_username(username=request_username)

		if user is None:
			raise ApiError(USER_API_ERRORS['USERNAME_NO_EXIST'])

	serialize_user = UserSchema(only=parsed_select_fields).dump
	serialized_user = serialize_user(user)

	return jsonify(serialized_user)


@app.route('/user/all', methods=['GET'])
def get_all_users():
	repo = UserRepo(postgresql_engine)
	user_service = UserUsecase(repo)

	request_params = request.args

	request_ids = request_params.get('ids')
	request_select_fields = request_params.get('select')
	request_filter_by = request_params.get('filter_by')

	valid_user_fields = UserDTO.__match_args__
	parsed_select_fields = parse_select(select_fields=request_select_fields, valid_fields=valid_user_fields)
	parsed_filter_by = parse_filter_by(filter_by=request_filter_by, valid_fields=valid_user_fields)

	if request_ids is not None:
		request_ids = tuple(request_ids.split(','))

		if not is_valid_ids(ids=request_ids):
			raise ApiError(API_ERRORS['INVALID_ID'])

	users = user_service.get_users(required_ids=request_ids, filter_by=parsed_filter_by)
	serialize_users = UserSchema(only=parsed_select_fields, many=True).dump
	serialized_users = serialize_users(users)

	return jsonify(serialized_users)


@app.route('/user', methods=['PATCH'])
@jwt_required()
def update_user():
	repo = UserRepo(postgresql_engine)
	user_service = UserUsecase(repo)
	user_id = get_jwt_identity()

	formdata = request.form.to_dict(flat=True)
	parsed_formdata = UpdateUserSchema().load(formdata)

	if len(parsed_formdata) == 0 and 'avatar' not in request.files:
		raise ApiError(API_ERRORS['EMPTY_FORMDATA']) 
	
	

	if 'username' in parsed_formdata:
		username = parsed_formdata['username']
		found_user = user_service.get_by_username(username=username)

		if found_user is not None:
			raise ApiError(USER_API_ERRORS['USERNAME_EXISTS'])

	if 'email' in parsed_formdata:
		email = parsed_formdata['email']

		if user_service.email_exists(email):
			raise ApiError(USER_API_ERRORS['EMAIL_EXISTS'])

	if 'avatar' in request.files:
		image_file = request.files['avatar'].read()

		if not is_valid_jpg(image_file):
			raise ApiError(API_ERRORS['INVALID_JPG'])

		avatar_source = f'/static/images/avatar{str(user_id)}.jpg'
		parsed_formdata['avatar'] = 'https://ilow-api.eugenv.ru' + avatar_source

		with open('./src' + avatar_source, 'wb') as file:
			file.write(image_file)

	update_dto = UserUpdateDTO(**parsed_formdata)
	updated_user = user_service.update_user(id=user_id, update_user_dto=update_dto)

	return jsonify(updated_user._asdict())



@app.route('/user', methods=['DELETE'])
@jwt_required()
def delete_user():
	repo = UserRepo(postgresql_engine)
	user_service = UserUsecase(repo)

	user_id = get_jwt_identity()

	deleted_user = user_service.delete_user(id=user_id)

	response = jsonify(deleted_user._asdict())
	unset_jwt_cookies(response)

	return response
