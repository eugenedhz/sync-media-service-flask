from typing import Optional
from redis import Redis

from src.interface.repository.socket_connection_session import (
	SocketConnectionSessionRepoInterface
)


class SocketConnectionSessionRepo(SocketConnectionSessionRepoInterface):
	def __init__(self, redis: Redis, group: str):
		self.redis = redis
		self.group = group
		

	def set(self, key: str | int, value: int | str) -> None:
		self.redis.hset(self.group, key, value)


	def get(self, key: str | int) -> Optional[int | str]:
		value = self.redis.hget(self.group, key)

		if value is None:
			return None
		try:
			user_id = int(value)
			return user_id
		except:
			user_sid = value
			return user_sid


	def delete(self, key: str) -> None:
		self.redis.hdel(self.group, key)


	def keys(self) -> tuple[str | int, ...]:
		keys = self.redis.hkeys(self.group)
		return tuple(keys)
