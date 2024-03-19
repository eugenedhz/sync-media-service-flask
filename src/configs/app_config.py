from datetime import timedelta
from os import getenv


class Default(object):
	TESTING = False

	JWT_TOKEN_LOCATION = ['cookies']
	JWT_COOKIE_SAMESITE = 'None'
	JWT_COOKIE_CSRF_PROTECT = False
	JWT_COOKIE_SECURE = True
	JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=10)
	JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)
	JWT_SECRET_KEY = getenv('JWT_SECRET_KEY')

	POSTGRES_CONN_URL = getenv('POSTGRES_CONN_URL')

	SWAGGER = {
        'uiversion': 3,
        'openapi': '3.0.2'
	}

	STATIC_IMAGES_FOLDER = './src/static/images/'
	STATIC_IMAGES_URL = '/static/images/'


class Development(Default):
	DEBUG = False

	JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
	JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=2)