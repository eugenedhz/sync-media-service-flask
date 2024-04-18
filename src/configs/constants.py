from datetime import timedelta

from pkg.constants.readonly import Readonly


class Role(Readonly):
	ADMIN = 'ADMIN'


class Regex(Readonly):
	USERNAME = r'^[a-zA-Z0-9._-]+$'
	PASSWORD = r'^[a-zA-Z0-9.@_-]+$'


class Static(Readonly):
	IMAGES_FOLDER = './src/static/images/'
	IMAGES_URL = '/static/images/'

	VIDEOS_FOLDER = './src/static/videos/'
	VIDEOS_URL = '/static/videos/'
	VIDEOS_QUALITIES = ('360p', '480p', '720p', '1080p')
	VIDEOS_TRANSCODED_EXTENSION = '.mp4'


class Session(Readonly):
	UPLOAD_GROUP = 'upload'
	UPLOAD_TIMEOUT = timedelta(minutes=1)
	UPLOAD_CLEANER_SLEEP = timedelta(seconds=30).total_seconds()

	TRANSCODE_GROUP = 'transcode'
	TRANSCODE_STATUS_EXPIRES = timedelta(minutes=1)
	TRANSCODE_STATUSES = {
		3: 'pending',
		2: 'processing',
		1: 'error',
		0: 'success'
	}
