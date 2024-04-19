from src.usecase.media.usecase import MediaUsecase
from src.repository.media.repo import MediaRepo
from src.repository.driver.postgres import postgresql_engine


repo = MediaRepo(postgresql_engine)
media_service = MediaUsecase(repo)