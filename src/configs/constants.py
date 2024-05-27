from pkg.constants.readonly import Readonly


class Role(Readonly):
	ADMIN = 'ADMIN'
	USER = 'USER'


class Regex(Readonly):
	USERNAME = r'^[a-zA-Z0-9._-]+$'
	PASSWORD = r'^[a-zA-Z0-9.@_-]+$'
	VIDEO = r'^[0-9a-z]+\.[a-z0-9]+$'
	ROOM_NAME = r'^[a-zA-Z0-9_]+$'


class Static(Readonly):
	IMAGES_FOLDER = './src/static/images/'
	IMAGES_URL = '/static/images/'


class Tables(Readonly):
	USER = 'User'
	MEDIA = 'Media'
	ROOM = 'Room'
