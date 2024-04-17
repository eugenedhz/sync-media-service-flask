from src.repository.driver.redis import redis
from src.repository.session.repo import SessionRepo
from src.configs.constants import Static, Session

from pkg.file.video.service import VideoService


upload_session = SessionRepo(redis, Session.UPLOAD_GROUP)
transcode_session = SessionRepo(redis, Session.TRANSCODE_GROUP)

video_service = VideoService(destination_path=Static.VIDEOS_FOLDER)
