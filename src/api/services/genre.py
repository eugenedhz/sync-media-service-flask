from src.usecase.genre.usecase import GenreUsecase
from src.repository.genre.repo import GenreRepo
from src.repository.driver.postgres import postgresql_engine


repo = GenreRepo(postgresql_engine)
genre_service = GenreUsecase(repo)