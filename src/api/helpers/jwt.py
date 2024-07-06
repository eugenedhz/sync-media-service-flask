from flask import jsonify
from flask_jwt_extended import get_jwt
from functools import wraps

from src.api.error.shared_error import API_ERRORS
from src.api.error.custom_error import ApiError


def role_required(role):
    def wrapper(fn):

        @wraps(fn)
        def decorator(*args, **kwargs):
            claims = get_jwt()

            if claims['role'] == role:
                return fn(*args, **kwargs)

            raise ApiError(API_ERRORS[f'{role}_RIGHTS_REQUIRED'])

        return decorator

    return wrapper