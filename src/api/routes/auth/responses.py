from flask import jsonify, Response
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token,
    set_access_cookies, 
    set_refresh_cookies
)

from src.configs.constants import Role


def create_response_with_jwt(user: dict, is_refresh: bool) -> Response:
	user_id = user['id']

	access_token = create_access_token(
		identity = user_id, 
		additional_claims = {Role.ADMIN: False}
	)

	refresh_token = create_refresh_token(
		identity = user_id, 
		additional_claims = {Role.ADMIN: False}
	)

	response = jsonify(user)
	set_access_cookies(response, access_token)

	if not is_refresh:
		set_refresh_cookies(response, refresh_token)

	return response
