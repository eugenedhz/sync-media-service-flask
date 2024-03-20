from src.usecase.user.usecase import UserUsecase
from src.repository.user.repo import UserRepo
from src.repository.driver.postgres import postgresql_engine


repo = UserRepo(postgresql_engine)
user_service = UserUsecase(repo)