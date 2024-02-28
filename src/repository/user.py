from sqlalchemy import Engine, update, select
from sqlalchemy.orm import Session
from typing import Union

from src.domain.user import User
from src.interface.repos.user import UserRepoInterface
from src.repository.sqla_models.models import User as UserModel


class UserRepo(UserRepoInterface):
	def __init__(self, engine: Engine):
		self.engine = engine


	def store(self, user: User) -> None:
		with Session(self.engine) as s:
			new_user = UserModel(**(user.to_dict()))

			s.add(new_user)

			s.commit()


	def get_by_id(self, id: Union[str | int]) -> User:
		with Session(self.engine) as s:
			found_user = s.get(UserModel, int(id))

		return User(**(found_user.__dict__))
			

	def get_by_username(self, username: str) -> User:
		with Session(self.engine) as s:
			found_user = s.execute(select(UserModel).filter_by(username=username))

		return User(**(found_user.__dict__))


	def update(self, user: User) -> None:
		with Session(self.engine) as s:
			query = (
				update(UserModel)
				.where(UserModel.id == int(user.id))
				.values(**(user.to_dict()))
			)

			updated_user = s.scalars(query)


	def get_all(self) -> list[User]:
		with Session(self.engine) as s:
			found_users = s.execute(select(UserModel).all())

		return [User(**(user.__dict__)) for user in found_users]


	def delete_user(self, id: Union[str | int]) -> User:
		with Session(self.engine) as s:
			found_user = s.get(UserModel, int(id))

			s.delete(found_user)

		return User(**(found_user.__dict__))


	def username_exists(self, username: str) -> bool:
		with Session(self.engine) as s:
			found_user = s.execute(select(UserModel).filter_by(username=username))

		return found_user is not None