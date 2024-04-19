from flask import jsonify, Response
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token,
    set_access_cookies, 
    set_refresh_cookies
)

from src.api.routes.auth.types import Claims
from src.configs.constants import Role


def create_response_with_jwt(user: dict, claims: Claims) -> Response:
	user_id = user['id']
	role = claims['role']
	is_refresh_request = (claims['type'] == 'refresh')

	token_info = {
		'identity': user_id,
		'additional_claims': {'role': role}
	}

	response = jsonify(user)

	access_token = create_access_token(**token_info)
	set_access_cookies(response, access_token)

	if not is_refresh_request:
		refresh_token = create_refresh_token(**token_info)
		set_refresh_cookies(response, refresh_token)

	return response
