from flask import request, jsonify
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity, set_access_cookies,
    unset_jwt_cookies, get_jwt
)

from src.app import app
from src.domain.user import User
from src.usecase.user.usecase import UserUsecase
from src.usecase.dto import QueryParametersDTO
from src.usecase.user.dto import UserDTO, UserUpdateDTO
from src.repository.user.repo import UserRepo
from src.repository.driver.postgres import postgresql_engine
from src.api.error.shared_error import API_ERRORS
from src.api.routes.user.error import USER_API_ERRORS
from src.api.error.custom_error import ApiError
from src.api.routes.user.schemas import UserSchema, UpdateUserSchema
from src.configs.constants import Role, Static

from pkg.query_params.select.parse import parse_select
from pkg.query_params.filter_by.parse import parse_filter_by
from pkg.query_params.ids.validate import is_valid_ids
from pkg.image.jpg_validate import is_valid_jpg
from pkg.file.file_service import FileService
from pkg.file.filename import get_filename, get_extension


@app.route('/user', methods=['GET'])
def get_user_by_username_or_id():
	repo = UserRepo(postgresql_engine)
	user_service = UserUsecase(repo)

	request_params = request.args

	username = request_params.get('username')
	user_id = request_params.get('id')

	if (username is None) and (user_id is None):
		raise ApiError(API_ERRORS['NO_IDENTITY_PROVIDED'])

	select = request_params.get('select')
	user_fields = UserDTO.__match_args__
	try:
		select = parse_select(select=select, valid_fields=user_fields)
	except:
		raise ApiError(API_ERRORS['INVALID_SELECT'])

	if user_id is not None:
		if not user_id.isdigit():
			raise ApiError(API_ERRORS['INVALID_ID'])

		user = user_service.get_by_id(id=user_id)

		if user is None:
			raise ApiError(USER_API_ERRORS['USER_NOT_FOUND'])

	else:
		user = user_service.get_by_username(username=username)

		if user is None:
			raise ApiError(USER_API_ERRORS['USER_NOT_FOUND'])

	serialize_user = UserSchema(only=select).dump
	serialized_user = serialize_user(user)

	return jsonify(serialized_user)


@app.route('/user/all', methods=['GET'])
def get_all_users():
	repo = UserRepo(postgresql_engine)
	user_service = UserUsecase(repo)

	request_params = request.args

	user_ids = request_params.get('ids')

	if user_ids is not None:
		user_ids = tuple(user_ids.split(','))

		if not is_valid_ids(ids=user_ids):
			raise ApiError(API_ERRORS['INVALID_ID'])

	select = request_params.get('select')
	filter_by = request_params.get('filter_by')

	user_fields = UserDTO.__match_args__
	try:
		select = parse_select(select=select, valid_fields=user_fields)
	except:
		raise ApiError(API_ERRORS['INVALID_SELECT'])

	# .__annotations__ возвращает словарь {поле: тип поля}
	user_fields = UserDTO.__annotations__
	try:
		filter_by = parse_filter_by(filter_query=filter_by, valid_fields=user_fields)
	except:
		raise ApiError(API_ERRORS['INVALID_FILTERS'])

	query_parameters = QueryParametersDTO(required_ids=user_ids, filters=filter_by)
	users = user_service.get_users(query_parameters)

	if len(users) == 0:
		raise ApiError(USER_API_ERRORS['USERS_NOT_FOUND'])

	serialize_users = UserSchema(only=select, many=True).dump
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

		username_exists = user_service.field_exists(name='username', value=username)
		if username_exists:
			raise ApiError(USER_API_ERRORS['USERNAME_EXISTS'])

	if 'email' in parsed_formdata:
		email = parsed_formdata['email']

		email_exists = user_service.field_exists(name='email', value=email)
		if email_exists:
			raise ApiError(USER_API_ERRORS['EMAIL_EXISTS'])

	if 'avatar' in request.files:
		image = request.files['avatar']
		data = image.read()
		extension = get_extension(image.filename)
		valid_extensions = Static.ALLOWED_IMAGE_EXTENSIONS

		if not(is_valid_jpg(data)) and not(extension in valid_extensions):
			raise ApiError(API_ERRORS['INVALID_JPG'])

		static_folder = Static.IMAGES_FOLDER
		static_url = Static.IMAGES_URL
		file_service = FileService(destination_path=static_folder)

		try:
			saved_filename = file_service.save(data=data, extension=extension)
		except:
			raise ApiError(API_ERRORS['CANT_SAVE_FILE'])

		user = user_service.get_by_id(user_id)
		avatar = user.avatar

		if avatar is not None:
			filename = get_filename(avatar)
			try:
				file_service.delete(filename)
			except:
				pass

		avatar_url = static_url + saved_filename
		parsed_formdata['avatar'] = avatar_url

	dto = UserUpdateDTO(**parsed_formdata)
	updated_user = user_service.update_user(id=user_id, update_user_dto=dto)

	return jsonify(updated_user._asdict())


@app.route('/user', methods=['DELETE'])
@jwt_required()
def delete_user():
	repo = UserRepo(postgresql_engine)
	user_service = UserUsecase(repo)

	request_params = request.args
	user_id = request_params.get('id')

	if user_id is None:
		raise ApiError(API_ERRORS['NO_IDENTITY_PROVIDED'])
	if not user_id.isdigit():
		raise ApiError(API_ERRORS['INVALID_ID'])

	user_id = int(user_id)
	jwt_user_id = int(get_jwt_identity())

	if user_id != jwt_user_id:
		claims = get_jwt()
		admin_rights = claims[Role.ADMIN]

		if not admin_rights:
			raise ApiError(API_ERRORS['ADMIN_RIGHTS_REQUIRED'])

	user_exists = user_service.field_exists(name='id', value=user_id)
	if not user_exists:
		raise ApiError(USER_API_ERRORS['USER_NOT_FOUND'])
			
	deleted_user = user_service.delete_user(id=user_id)
	avatar = deleted_user.avatar

	if avatar is not None:
		static_folder = Static.IMAGES_FOLDER
		file_service = FileService(destination_path=static_folder)
		
		filename = get_filename(avatar)
		try:
			file_service.delete(filename)
		except:
			pass

	return deleted_user._asdict()
