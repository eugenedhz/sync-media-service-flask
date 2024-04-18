from src.app import app

import src.api.error.app_errors
import src.api.error.jwt_errors

import src.api.routes.user.controller
import src.api.routes.auth.controller
import src.api.routes.video.controller

from src.threads.video.transcoder import transcoder
from src.threads.video.cleaner import cleaner


if __name__ == '__main__':
	app.run(port='5173')