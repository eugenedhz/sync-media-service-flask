from src.app import app

import src.api.error.app_errors
import src.api.error.jwt_errors

import src.api.routes.user.controller
import src.api.routes.auth.controller
<<<<<<< HEAD
import src.api.routes.video.controller

from src.threads.video.transcoder import transcoder
from src.threads.video.cleaner import cleaner
=======
import src.api.routes.media.controller
>>>>>>> 4bb141bf265b70ae442782c67f21388f2788f235


if __name__ == '__main__':
	app.run(port='8302')