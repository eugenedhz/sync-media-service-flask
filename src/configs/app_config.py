from datetime import timedelta


class Default(object):
	TESTING = False

	JWT_TOKEN_LOCATION = ['cookies']
	JWT_COOKIE_SAMESITE = 'None'
	JWT_COOKIE_CSRF_PROTECT = False
	JWT_COOKIE_SECURE = True
	JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=10)
	JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)
	JWT_SECRET_KEY = "NeeDs2BeR3PlacEd" # TODO: get from the env variables

	SWAGGER = {
        'uiversion': 3,
        'openapi': '3.0.2'
	}

	# TODO: get password and username from the env variables
	POSTGRES_CONN_URL = 'postgresql://postgres:test3915@eugenv.ru/ilow' 


class Development(Default):
	DEBUG = False

	JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
	JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=2)