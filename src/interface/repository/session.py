from abc import ABC, abstractmethod
from typing import Union, Optional


Key = Union[str, int, float]
Value = Union[str, int, float]


class SessionRepoInterface(ABC):
	@abstractmethod
	def set(self, key: Key, value: Value) -> None:
		raise NotImplementedError


	@abstractmethod
	def get(self, key: Key) -> Optional[Value]:
		raise NotImplementedError


	@abstractmethod
	def delete(self, key: Key) -> None:
		raise NotImplementedError


	@abstractmethod
	def keys(self) -> tuple[Key, ...]:
		raise NotImplementedError
