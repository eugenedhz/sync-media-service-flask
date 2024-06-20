from src.usecase.playlist_media.usecase import PlaylistMediaUsecase
from src.repository.playlist_media.repo import PlaylistMediaRepo
from src.repository.driver.postgres import postgresql_engine


repo = PlaylistMediaRepo(postgresql_engine)
playlist_media_service = PlaylistMediaUsecase(repo)