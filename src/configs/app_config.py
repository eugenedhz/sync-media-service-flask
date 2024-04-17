from datetime import timedelta

from pkg.constants.env import get_from_env


class Default(object):
	TESTING = False

	JWT_TOKEN_LOCATION = ['cookies']
	JWT_COOKIE_SAMESITE = 'None'
	JWT_COOKIE_CSRF_PROTECT = False
	JWT_COOKIE_SECURE = True
	JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=10)
	JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)
	JWT_SECRET_KEY = get_from_env('JWT_SECRET_KEY')
	
	POSTGRES_CONN_URL = get_from_env('POSTGRES_CONN_URL')
	REDIS_CONN_URL = get_from_env('REDIS_CONN_URL')

	SWAGGER = {
        'uiversion': 3,
        'openapi': '3.0.2'
	}
	

class Development(Default):
	DEBUG = False

	JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
	JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=2)