from sqlalchemy import Engine, update, select
from sqlalchemy.orm import Session
from typing import Union

from src.domain.user import User
from src.interface.repository.user import UserRepoInterface
from src.repository.sqla_models.models import UserModel


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
			found_user = s.get(UserModel, id)

			found_user_dict = found_user.__dict__
			del found_user_dict['_sa_instance_state']

		return User(**found_user_dict)
			

	def get_by_username(self, username: str) -> User:
		with Session(self.engine) as s:
			found_user = s.execute(select(UserModel).filter_by(username=username))

			found_user_dict = found_user.__dict__
			del found_user_dict['_sa_instance_state']

		return User(**found_user_dict)


	def update(self, user: User) -> None:
		with Session(self.engine) as s:
			query = (
				update(UserModel)
				.where(UserModel.id == int(user.id))
				.values(**(user.to_dict()))
			)

			s.scalars(query)


	def get_all(self) -> list[User]:
		with Session(self.engine) as s:
			found_users = s.execute(select(UserModel).all())

			found_dict_users = [user.__dict__ for user in found_users]

			for user in found_users_dict:
				del user['_sa_instance_state']

		return [User(**user) for user in found_dict_users]


	def delete_user(self, id: Union[str | int]) -> User:
		with Session(self.engine) as s:
			found_user = s.get(UserModel, id)

			found_user_dict = found_user.__dict__

			del found_user_dict['_sa_instance_state']

			s.delete(found_user)

		return User(**found_user_dict)


	def username_exists(self, username: str) -> bool:
		with Session(self.engine) as s:
			found_user = s.execute(select(UserModel).filter_by(username=username))

		return found_user is not None