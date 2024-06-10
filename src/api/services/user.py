from src.usecase.user.usecase import UserUsecase
from src.repository.user.repo import UserRepo
from src.repository.socket_connection_session.repo import SocketConnectionSessionRepo
from src.repository.driver.postgres import postgresql_engine
from src.repository.driver.redis import redis

from src.configs.constants import RedisGroups



repo = UserRepo(postgresql_engine)
user_service = UserUsecase(repo)
user_socket_session = SocketConnectionSessionRepo(redis, RedisGroups.SOCKET_CONNECTION)