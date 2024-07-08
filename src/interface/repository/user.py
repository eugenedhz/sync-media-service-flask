from abc import ABC, abstractmethod
from typing import Any

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
	def get_all(self, query_parameters_dto: QueryParametersDTO) -> list[UserDTO]:
		raise NotImplementedError


	@abstractmethod
	def delete(self, id: int) -> User:
		raise NotImplementedError


	def is_admin(self, user_id: int) -> bool:
		raise NotImplementedError


	@abstractmethod
	def is_field_exists(self, field: dict[str: Any]) -> bool:
		raise NotImplementedError
