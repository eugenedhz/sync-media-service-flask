from src.interface.repos.user import UserRepoInterface
from src.usecase.exception.base_exception import BaseError
from src.domain.user import User

from typing import Union
import datetime


class UserUsecase():

	def __init__(self, repo: UserRepoInterface):
		self.repo = repo


	# TODO: решить вопрос с ошибками, их хендлингом и пробросом во внешний слой API
	def register(self, username: str, password_hash: str) -> Union[User | BaseError]:
		new_user = User(
			username = username,
			password_hash = password_hash,
			registration_date = datetime.date.now()
		)

		repo.store(new_user)

		return new_user


	