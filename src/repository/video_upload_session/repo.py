from typing import Optional
from redis import Redis

from src.interface.repository.video_upload_session import (
	VideoUploadSessionRepoInterface, Key, Value
)


class VideoUploadSessionRepo(VideoUploadSessionRepoInterface):
	def __init__(self, redis: Redis, group: str):
		self.redis = redis
		self.group = group
		

	def set(self, key: Key, value: Value) -> None:
		self.redis.hset(self.group, key, value)


	def get(self, key: Key) -> Optional[Value]:
		value = self.redis.hget(self.group, key)
		if not value:
			return None

		if value.replace('.', '', 1).isdigit():
			try:
				return int(value)
			except:
				return float(value)

		return value


	def delete(self, key: Key) -> None:
		self.redis.hdel(self.group, key)


	def keys(self) -> tuple[Key, ...]:
		keys = self.redis.hkeys(self.group)

		return tuple(keys)
