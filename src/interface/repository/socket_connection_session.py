from abc import ABC, abstractmethod
from typing import Union, Optional


class SocketConnectionSessionRepoInterface(ABC):
	@abstractmethod
	def set(self, request_sid: str, user_id: int) -> None:
		raise NotImplementedError


	@abstractmethod
	def get(self, request_sid: str) -> Optional[int]:
		raise NotImplementedError


	@abstractmethod
	def delete(self, request_sid: str) -> None:
		raise NotImplementedError


	@abstractmethod
	def keys(self) -> tuple[str, ...]:
		raise NotImplementedError