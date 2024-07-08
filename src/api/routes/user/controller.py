from flask import request, jsonify
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity, set_access_cookies,
    unset_jwt_cookies, get_jwt
)

from src.app import app
from src.api.services.user import user_service
from src.api.services.room import room_service
from src.api.services.image import image_service
from src.usecase.dto import QueryParametersDTO
from src.usecase.user.dto import UserDTO, UserUpdateDTO
from src.api.error.shared_error import API_ERRORS
from src.api.routes.user.error import USER_API_ERRORS
from src.api.error.custom_error import ApiError
from src.api.routes.user.schemas import UserSchema, UpdateUserSchema
from src.api.routes.room.schemas import RoomSchema
from src.configs.constants import Role, Static

from pkg.query_params.select.parse import parse_select
from pkg.query_params.filter_by.parse import parse_filter_by
from pkg.query_params.expand.parse import parse_expand
from pkg.query_params.ids.validate import is_valid_ids
from pkg.file.image.jpg_validate import is_valid_jpg
from pkg.file.filename import split_filename


EXPAND_FIELDS = ('createdRooms', 'friends')


@app.route('/user', methods=['GET'])
def get_user_by_username_or_id():
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

	expand = request_params.get('expand')
	try:
		expand = parse_expand(expand=expand, valid_fields=EXPAND_FIELDS)
	except:
		raise ApiError(API_ERRORS['INVALID_EXPAND'])

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

	expand = request_params.get('expand')

	try:
		expand = parse_expand(expand=expand, valid_fields=EXPAND_FIELDS)
	except:
		raise ApiError(API_ERRORS['INVALID_EXPAND'])

	serialize_user = UserSchema(only=select).dump
	serialize_users = UserSchema(only=select, many=True).dump
	serialized_user = serialize_user(user)

	if not expand:
		return jsonify(serialized_user)

	if 'createdRooms' in expand:
		created_rooms = room_service.get_creator_rooms(user.id)
		serialize_rooms = RoomSchema(many=True).dump
		serialized_user['createdRooms'] = serialize_rooms(created_rooms)

	if 'friends' in expand:
		friends = user_service.get_friends(user_id=user_id)
		serialized_user['friends'] = serialize_users(friends)

	return jsonify(serialized_user)


@app.route('/user/all', methods=['GET'])
def get_all_users():
	request_params = request.args

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

	expand = request_params.get('expand')
	try:
		expand = parse_expand(expand=expand, valid_fields=EXPAND_FIELDS)
	except:
		raise ApiError(API_ERRORS['INVALID_EXPAND'])

	limit = request_params.get('limit')
	offset = request_params.get('offset')
	if limit or offset:
		try:
			limit = int(limit)
			offset = int(offset)
		except:
			raise ApiError(API_ERRORS['INVALID_PAGE_QUERY'])

	query_parameters_dto = QueryParametersDTO(filters=filter_by, limit=limit, offset=offset)
	users = user_service.get_users(query_parameters_dto=query_parameters_dto)

	if len(users) == 0:
		return jsonify([])

	expand = request_params.get('expand')

	try:
		expand = parse_expand(expand=expand, valid_fields=EXPAND_FIELDS)
	except:
		raise ApiError(API_ERRORS['INVALID_EXPAND'])

	serialize_users = UserSchema(only=select, many=True).dump

	serialized_users = serialize_users(users)

	if not expand:
		return jsonify(serialized_users)

	if 'createdRooms' in expand:
		serialize_rooms = RoomSchema(many=True).dump
		for i in range(len(users)):
			user_id = users[i].id
			created_rooms = room_service.get_creator_rooms(user_id)
			serialized_users[i]['createdRooms'] = serialize_rooms(created_rooms)

	if 'friends' in expand:
		for user in serialized_users:
			friends = user_service.get_friends(user_id=user['id'])
			user['friends'] = serialize_users(friends)

	return jsonify(serialized_users)


@app.route('/user', methods=['PATCH'])
@jwt_required()
def update_user():
	user_id = get_jwt_identity()
	is_user_exists = user_service.is_field_exists(name='id', value=int(user_id))

	if not is_user_exists:
		raise ApiError(USER_API_ERRORS['USER_NOT_FOUND'])

	formdata = UpdateUserSchema().load(request.form)

	if len(formdata) == 0 and 'avatar' not in request.files:
		raise ApiError(API_ERRORS['EMPTY_FORMDATA']) 

	if 'username' in formdata:
		username = formdata['username']

		is_username_exists = user_service.is_field_exists(name='username', value=username)
		if is_username_exists:
			raise ApiError(USER_API_ERRORS['USERNAME_EXISTS'])

	if 'email' in formdata:
		email = formdata['email']

		is_email_exists = user_service.is_field_exists(name='email', value=email)
		if is_email_exists:
			raise ApiError(USER_API_ERRORS['EMAIL_EXISTS'])

	if 'avatar' in request.files:
		image = request.files['avatar']
		data = image.read()
		extension = split_filename(image.filename).extension

		if not is_valid_jpg(data, extension):
			raise ApiError(API_ERRORS['INVALID_JPG'])

		try:
			saved_filename = image_service.save(data=data, extension=extension)
		except:
			raise ApiError(API_ERRORS['CANT_SAVE_FILE'])

		user = user_service.get_by_id(user_id)
		avatar = user.avatar

		if avatar is not None:
			filename = split_filename(avatar).filename()
			try:
				image_service.delete(filename)
			except:
				pass

		avatar_url = Static.IMAGES_URL + saved_filename
		formdata['avatar'] = avatar_url

	dto = UserUpdateDTO(**formdata)
	updated_user = user_service.update_user(id=user_id, update_user_dto=dto)

	return jsonify(updated_user._asdict())


@app.route('/user', methods=['DELETE'])
@jwt_required()
def delete_user():
	user_id = request.args.get('id')

	if user_id is None:
		raise ApiError(API_ERRORS['NO_IDENTITY_PROVIDED'])
	if not user_id.isdigit():
		raise ApiError(API_ERRORS['INVALID_ID'])

	user_id = int(user_id)
	jwt_user_id = int(get_jwt_identity())

	if user_id != jwt_user_id:
		claims = get_jwt()
		role = claims['role']

		if role != Role.ADMIN:
			raise ApiError(API_ERRORS['ADMIN_RIGHTS_REQUIRED'])

	is_user_exists = user_service.is_field_exists(name='id', value=user_id)
	if not is_user_exists:
		raise ApiError(USER_API_ERRORS['USER_NOT_FOUND'])

	images = []
	created_rooms = room_service.get_creator_rooms(user_id)
	for room in created_rooms:
		if room.cover:
			images.append(room.cover)
	
	user = user_service.delete_user(id=user_id)
	if user.avatar:
		images.append(user.avatar)

	for image in images:
		filename = split_filename(image).filename()
		try:
			image_service.delete(filename)
		except:
			pass

	return jsonify(user._asdict())
