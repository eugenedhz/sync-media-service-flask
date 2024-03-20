from pkg.constants.readonly import Readonly


class Role(Readonly):
	ADMIN = 'ADMIN'


class Regex(Readonly):
	USERNAME = r'^[a-zA-Z0-9._-]+$'
	PASSWORD = r'^[a-zA-Z0-9.@_-]+$'


class Static(Readonly):
	IMAGES_FOLDER = './src/static/images/'
	IMAGES_URL = '/static/images/'
	ALLOWED_IMAGE_EXTENSIONS = ('.jpg', '.jpeg')
