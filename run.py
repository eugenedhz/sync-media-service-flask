from src.app import app

import src.api.error.app_errors
import src.api.error.jwt_errors
import src.api.routes.user.controller


if __name__ == '__main__':
	app.run(port='8302')
