from datetime import timedelta

from pkg.constants.readonly import Readonly


class Role(Readonly):
	ADMIN = 'ADMIN'
	USER = 'USER'


class Regex(Readonly):
	USERNAME = r'^[a-zA-Z0-9._-]+$'
	PASSWORD = r'^[a-zA-Z0-9.@_-]+$'
	VIDEO = r'^[0-9a-z]+\.[a-z0-9]+$'
	COUNTRY_CODE = r'^[A-Z]{2}$'
	ROOM_NAME = r'^[a-zA-Z0-9_]+$'
	GENRE_NAME = r'^[А-Я]{1}[а-я]+$'
	GENRE_SLUG = r'^[a-z]+$'


class Static(Readonly):
	IMAGES_FOLDER = './src/static/images/'
	IMAGES_URL = '/static/images/'

	VIDEOS_FOLDER = './src/static/videos/'
	VIDEOS_URL = '/static/videos/'
	VIDEOS_QUALITIES = ('360p', '480p', '720p', '1080p')
	VIDEOS_TRANSCODED_EXTENSION = '.mp4'


class Tables(Readonly):
	USER = 'User'
	MEDIA = 'Media'
	MEDIA_VIDEO = 'Video'
	ROOM = 'Room'
	GENRE = 'Genre'
	MEDIA_GENRE = 'MediaGenre'
	FRIENDSHIP_REQUEST = 'FriendshipRequest'
	FRIENDSHIP = 'Friendship'


class VideoUploadSession(Readonly):
	CLEANER_SLEEP = timedelta(days=1).total_seconds()
	
	UPLOAD_GROUP = 'upload'
	UPLOAD_TIMEOUT = timedelta(days=1)

	TRANSCODE_GROUP = 'transcode'
	TRANSCODE_STATUS_EXPIRES = timedelta(days=1)
	TRANSCODE_STATUSES = {
		3: 'pending',
		2: 'processing',
		1: 'error',
		0: 'success',
		None: 'expired'
	}