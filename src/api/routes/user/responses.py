from flask import jsonify, Response
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token,
    set_access_cookies, 
    set_refresh_cookies
)


def create_response_with_jwt(response_user: dict) -> Response:
	user_id = response_user['id']

	access_token = create_access_token(
		identity = user_id, 
		additional_claims = {'ADMIN': False}
	)

	refresh_token = create_refresh_token(
		identity = user_id, 
		additional_claims = {'ADMIN': False}
	)

	response = jsonify(response_user)
	set_access_cookies(response, access_token)
	set_refresh_cookies(response, refresh_token)

	return response
