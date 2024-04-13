from pkg.constants.readonly import Readonly


class Role(Readonly):
	ADMIN = 'ADMIN'


class Regex(Readonly):
	USERNAME = r'^[a-zA-Z0-9._-]+$'
	PASSWORD = r'^[a-zA-Z0-9.@_-]+$'
	TRAILER = r'^[0-9a-z]+\.[a-z0-9]+$'


class Static(Readonly):
	IMAGES_FOLDER = './src/static/images/'
	IMAGES_URL = '/static/images/'


class MediaFiles(Readonly):
	FILES = ('preview', 'thumbnail')
