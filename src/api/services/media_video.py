from src.usecase.media_video.usecase import MediaVideoUsecase
from src.repository.media_video.repo import MediaVideoRepo
from src.repository.driver.postgres import postgresql_engine


repo = MediaVideoRepo(postgresql_engine)
media_video_service = MediaVideoUsecase(repo)