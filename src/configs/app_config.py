from datetime import timedelta


class Default(object):
	TESTING = False

	JWT_TOKEN_LOCATION = ['cookies']
	JWT_COOKIE_SAMESITE = 'None'
	JWT_COOKIE_CSRF_PROTECT = False
	JWT_COOKIE_SECURE = True
	JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
	JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
	JWT_SECRET_KEY = "" # TODO: get from the env variables

	SWAGGER = {
        'uiversion': 3,
        'openapi': '3.0.2'
	}

	# TODO: get password and username from the env variables
	POSTGRES_CONN_URL = 'postgresql://postgres:test3915@localhost/ilow' 


class Development(Default):

	JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=1)
	JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=2)