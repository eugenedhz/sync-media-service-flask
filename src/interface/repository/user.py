from abc import ABC, abstractmethod
from src.usecase.user.dto import UserUpdateDTO
from typing import Union, Optional
from src.domain.user import User


class UserRepoInterface(ABC):

	@abstractmethod
	def store(self, user: User) -> User:
		raise NotImplementedError


	@abstractmethod
	def get_by_id(self, id: str, select_fields: Optional[tuple[str, ...]]) -> User:
		raise NotImplementedError


	@abstractmethod
	def get_by_username(self, username: str, select_fields: Optional[tuple[str, ...]]) -> User:
		raise NotImplementedError


	@abstractmethod
	def update(self, id: Union[str, int], update_user_dto: UserUpdateDTO) -> User:
		raise NotImplementedError


	@abstractmethod
	def get_all(self, select_fields: Optional[tuple[str, ...]], required_ids: Optional[tuple[int | str, ...]]) -> list[dict]:
		raise NotImplementedError


	@abstractmethod
	def delete(self, id: str) -> User:
		raise NotImplementedError


	@abstractmethod
	def email_exists(self, email: str) -> bool:
		raise NotImplementedError

