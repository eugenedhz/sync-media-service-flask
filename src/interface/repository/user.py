from abc import ABC, abstractmethod
from typing import Union, Optional, Any

from src.usecase.dto import QueryParametersDTO
from src.usecase.user.dto import UserUpdateDTO, UserDTO
from src.domain.user import User


class UserRepoInterface(ABC):
	@abstractmethod
	def store(self, user: User) -> User:
		raise NotImplementedError


	@abstractmethod
	def get_by_id(self, id: int) -> User:
		raise NotImplementedError


	@abstractmethod
	def get_by_username(self, username: str) -> User:
		raise NotImplementedError


	@abstractmethod
	def update(self, id: int, update_user_dto: UserUpdateDTO) -> User:
		raise NotImplementedError


	@abstractmethod
	def get_all(self, query_parameters: QueryParametersDTO) -> list[UserDTO]:
		raise NotImplementedError


	@abstractmethod
	def delete(self, id: int) -> User:
		raise NotImplementedError


	@abstractmethod
	def field_exists(self, name: str, value: str) -> bool:
		raise NotImplementedError

