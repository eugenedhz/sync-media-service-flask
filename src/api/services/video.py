from src.repository.driver.redis import redis
from src.repository.video_upload_session.repo import VideoUploadSessionRepo
from src.configs.constants import Static, RedisGroups

from pkg.file.video.service import VideoService


upload_session = VideoUploadSessionRepo(redis, RedisGroups.UPLOAD)
transcode_session = VideoUploadSessionRepo(redis, RedisGroups.TRANSCODE)

video_service = VideoService(destination_path=Static.VIDEOS_FOLDER)
