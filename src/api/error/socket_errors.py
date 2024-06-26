from flask_socketio import emit

from src.api.extensions import socketio
from src.api.error.custom_error import ApiError


@socketio.on_error_default
def default_error_handler(error: ApiError):
	emit('error', error.to_dict())
