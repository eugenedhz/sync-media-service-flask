from abc import ABC, abstractmethod
from src.domain.user import User


class UserRepoInterface(ABC):

	@abstractmethod
	def store(self, user: User) -> User:
		raise NotImplementedError


	@abstractmethod
	def get_by_id(self, id: str) -> User:
		raise NotImplementedError


	@abstractmethod
	def get_by_username(self, username: str) -> User:
		raise NotImplementedError


	@abstractmethod
	def update(self, user: User) -> User:
		raise NotImplementedError


	@abstractmethod
	def get_all(self) -> list[User]:
		raise NotImplementedError


	@abstractmethod
	def delete_user(self, id: str) -> User:
		raise NotImplementedError

	
	@abstractmethod
	def username_exists(self, username: str) -> bool:
		raise NotImplementedError
