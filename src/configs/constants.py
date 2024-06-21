from pkg.constants.readonly import Readonly


class Role(Readonly):
	ADMIN = 'ADMIN'
	USER = 'USER'


class Regex(Readonly):
	USERNAME = r'^[a-zA-Z0-9._-]+$'
	PASSWORD = r'^[a-zA-Z0-9.@_-]+$'
	VIDEO = r'^[0-9a-z]+\.[a-z0-9]+$'
	GENRE_NAME = r'^[А-Я]{1}[а-я]+$'
	GENRE_SLUG = r'^[a-z]+$'


class Static(Readonly):
	IMAGES_FOLDER = './src/static/images/'
	IMAGES_URL = '/static/images/'


class Tables(Readonly):
	USER = 'User'
	MEDIA = 'Media'
	GENRE = 'Genre'
	MEDIA_GENRE = 'MediaGenre'
