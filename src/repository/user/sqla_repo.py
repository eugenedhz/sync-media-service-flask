from sqlalchemy import Engine, update, select
from sqlalchemy.orm import Session
from typing import Union

from src.domain.user import User
from src.interface.repository.user import UserRepoInterface
from src.repository.sqla_models.models import UserModel


class UserRepo(UserRepoInterface):
	def __init__(self, engine: Engine):
		self.engine = engine


	def store(self, user: User) -> User:
		with Session(self.engine, expire_on_commit=False) as s:
			new_user = UserModel(**(user.to_dict()))

			s.add(new_user)

			s.commit()
		
		return User(**new_user._asdict(User))


	def get_by_id(self, id: Union[str | int]) -> User:
		with Session(self.engine) as s:
			found_user = s.get(UserModel, id)

		return User(**found_user._asdict(User))
			

	def get_by_username(self, username: str) -> User:
		with Session(self.engine) as s:
			query = (
				select(UserModel)
				.filter_by(username=username)
			)

			found_user = s.scalars(query).first()

		return User(**found_user._asdict(User))


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
			query = (
				select(UserModel)
				.all()
			)

			found_users = s.scalars(query)

		found_users_dict = [user._asdict(User) for user in found_users]

		return [User(**user) for user in found_users_dict]


	def delete_user(self, id: Union[str | int]) -> User:
		with Session(self.engine) as s:
			found_user = s.get(UserModel, id)

			s.delete(found_user)

			s.commit()

		return User(**found_user._asdict(User))


	def username_exists(self, username: str) -> bool:
		with Session(self.engine) as s:
			query = (
				select(UserModel.id)
				.filter_by(username=username)
			)

			found_user = s.scalars(query).first()

		return found_user is not None


	def email_exists(self, email: str) -> bool:
		with Session(self.engine) as s:
			query = (
				select(UserModel.id)
				.filter_by(email=email)
			)

			found_user = s.scalars(query).first()

		return found_user is not None