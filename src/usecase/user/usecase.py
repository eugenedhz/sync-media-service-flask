from typing import Union
import datetime

from src.domain.user import User
from src.interface.repository.user import UserRepoInterface


class UserUsecase():

	def __init__(self, repo: UserRepoInterface):
		self.repo = repo


	def register(self, username: str, passwordHash: str) -> User:
		new_user = User(
			username = username,
			passwordHash = passwordHash,
			registrationDate = datetime.date.today()
		)

		self.repo.store(new_user)

		return new_user


	def get_by_id(self, id: str) -> User:
		found_user = self.repo.get_by_id(id = id)

		return found_user


	def username_exists(self, username: str) -> bool:
		exists = self.repo.username_exists(username)

		return exists