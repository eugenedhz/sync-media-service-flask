from src.api.services.video import video_service
from src.configs.constants import Static
from src.api.error.custom_error import ApiError
from src.api.routes.video.error import VIDEO_API_ERRORS

from pkg.file.filename import split_filename


def get_video_url(filename: str) -> str:
	name = split_filename(filename).name

	if video_service.find_file(name) is None:
		raise ApiError(VIDEO_API_ERRORS['VIDEO_NOT_FOUND'])

	return Static.VIDEOS_URL + filename


def get_videos_with_quality(filename: str) -> list[str]:
	name = split_filename(filename).name
	extension = Static.VIDEOS_TRANSCODED_EXTENSION
	filenames = []

	for quality in Static.VIDEOS_QUALITIES:
		filename = f'{ name }{ quality }{ extension }'
		filenames.append(filename)

	return filenames


def delete_videos_with_quality(filename: str) -> None:
	filenames = get_videos_with_quality(filename)

	for filename in filenames:
		try:
			video_service.delete(filename)
		except:
			pass