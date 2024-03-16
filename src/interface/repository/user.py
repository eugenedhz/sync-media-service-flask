from abc import ABC, abstractmethod
from src.usecase.user.dto import UserUpdateDTO
from typing import Union, Optional
from src.domain.user import User


class UserRepoInterface(ABC):

	@abstractmethod
	def store(self, user: User) -> User:
		raise NotImplementedError


	@abstractmethod
	def get_by_id(self, id: Union[str | int]) -> User:
		raise NotImplementedError


	@abstractmethod
	def get_by_username(self, username: str) -> User:
		raise NotImplementedError


	@abstractmethod
	def update(self, id: Union[str, int], update_user_dto: UserUpdateDTO) -> User:
		raise NotImplementedError


	@abstractmethod
	get_all(self, required_ids: Optional[tuple[int | str, ...]], filter_by: Optional[dict[str, Any]]) -> list[UserDTO]:
		raise NotImplementedError


	@abstractmethod
	def delete(self, id: Union[str | int]) -> User:
		raise NotImplementedError


	@abstractmethod
	def email_exists(self, email: str) -> bool:
		raise NotImplementedError

