from flask import jsonify

from src.api.extensions import jwt


@jwt.invalid_token_loader
def invalid_token_callback(error_string):
    return jsonify(message='INVALID_TOKEN'), 422


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify(message='TOKEN_HAS_EXPIRED'), 401


@jwt.unauthorized_loader
def unauthorized_callback(error_string):
    return jsonify(message='NO_TOKEN_PROVIDED'), 401


@jwt.needs_fresh_token_loader
def no_fresh_token_callback(jwt_header, jwt_payload):
    return jsonify(message='NO_FRESH_TOKEN_PROVIDED'), 401