from flask import jsonify

from src.app import app
from src.api.error.custom_error import ApiError


@app.errorhandler(ApiError) # handles all kinds of custom errors (executes with `raise ApiError({some data})`)
def error_response_callback(error):
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(404)
def error_response_callback(error):
    return jsonify(message='RESOURCE_NOT_FOUND'), 404


@app.errorhandler(405)
def error_response_callback(error):
    return jsonify(message='METHOD_NOT_ALLOWED'), 405


@app.errorhandler(500)
def error_response_callback(error):
    return jsonify(message='INTERNAL_SERVER_ERROR'), 500