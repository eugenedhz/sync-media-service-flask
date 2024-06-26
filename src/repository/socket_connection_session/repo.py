from typing import Optional
from redis import Redis

from src.interface.repository.socket_connection_session import (
	SocketConnectionSessionRepoInterface
)


class SocketConnectionSessionRepo(SocketConnectionSessionRepoInterface):
	def __init__(self, redis: Redis, group: str):
		self.redis = redis
		self.group = group
		

	def set(self, request_sid: str, user_id: int) -> None:
		self.redis.hset(self.group, request_sid, user_id)


	def get(self, request_sid: str) -> Optional[int]:
		user_id = self.redis.hget(self.group, request_sid)
		if user_id is None:
			return None

		return int(user_id)


	def delete(self, request_sid: str) -> None:
		self.redis.hdel(self.group, request_sid)


	def keys(self) -> tuple[str, ...]:
		keys = self.redis.hkeys(self.group)
		return tuple(keys)
