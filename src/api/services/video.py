from src.repository.driver.redis import redis
from src.repository.video_upload_session.repo import VideoUploadSessionRepo
from src.configs.constants import Static, VideoUploadSession

from pkg.file.video.service import VideoService


upload_session = VideoUploadSessionRepo(redis, VideoUploadSession.UPLOAD_GROUP)
transcode_session = VideoUploadSessionRepo(redis, VideoUploadSession.TRANSCODE_GROUP)

video_service = VideoService(destination_path=Static.VIDEOS_FOLDER)
