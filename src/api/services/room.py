from src.usecase.room.usecase import RoomUsecase
from src.repository.room.repo import RoomRepo
from src.repository.driver.postgres import postgresql_engine


repo = RoomRepo(postgresql_engine)
room_service = RoomUsecase(repo)