from typing import Union
import datetime

from src.domain.user import User
from src.usecase.user.dto import UserRegisterDTO
from src.interface.repository.user import UserRepoInterface


class UserUsecase():

	def __init__(self, repo: UserRepoInterface):
		self.repo = repo


	def register(self, user_dto: UserRegisterDTO) -> User:
		new_user = User(
			**(user_dto._asdict()),
			registrationDate = datetime.date.today()
		)

		stored_user = self.repo.store(new_user)

		return stored_user


	def get_by_username(self, username: str) -> User:
		found_user = self.repo.get_by_username(username=username)

		return found_user


	def get_by_id(self, id: str) -> User:
		found_user = self.repo.get_by_id(id=id)

		return found_user


	def delete_user(self, id: str) -> User:
		deleted_user = self.repo.delete_user(id=id)

		return deleted_user


	def username_exists(self, username: str) -> bool:
		exists = self.repo.username_exists(username)

		return exists


	def email_exists(self, email: str) -> bool:
		exists = self.repo.email_exists(email)

		return exists