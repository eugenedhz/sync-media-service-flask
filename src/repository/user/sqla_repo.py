from sqlalchemy import Engine, update, select
from sqlalchemy.orm import Session, defer
from typing import Union, Optional, Any

from src.domain.user import User
from src.interface.repository.user import UserRepoInterface
from src.repository.sqla_models.models import UserModel
from src.usecase.user.dto import UserUpdateDTO, UserDTO


class UserRepo(UserRepoInterface):
	def __init__(self, engine: Engine):
		self.engine = engine


	def store(self, user: User) -> User:
		with Session(self.engine) as s:
			new_user = UserModel(**(user.to_dict()))

			s.add(new_user)

			s.commit()

			s.refresh(new_user)
		
		return User(**new_user._asdict(User))


	def get_by_id(self, id: Union[str | int]) -> User:

		with Session(self.engine) as s:
			query = (
				select(UserModel)
				.where(UserModel.id == id)
			)

			found_user = s.scalars(query).first()

		if found_user is None:
			return None

		return User(**found_user._asdict(User))
			

	def get_by_username(self, username: str) -> User:

		with Session(self.engine) as s:
			query = (
				select(UserModel)
				.where(UserModel.username == username)
			)

			found_user = s.scalars(query).first()

		if found_user is None:
			return None

		return User(**found_user._asdict(User))


	def update(self, id: Union[str, int], update_user_dto: UserUpdateDTO) -> User:
		with Session(self.engine) as s:
			query = (
				update(UserModel)
				.where(UserModel.id == id)
				.values(**update_user_dto)
				.returning(UserModel)
			)

			s.execute(query)

			s.commit()

			updated_user = s.get(UserModel, id)

		return User(**updated_user._asdict(User))


	def get_all(self, required_ids: Optional[tuple[int | str, ...]], filter_by: Optional[dict[str, Any]]) -> list[UserDTO]:
		with Session(self.engine) as s:
			query = (
				select(UserModel)
				.options(defer(UserModel.passwordHash))
			)

			if required_ids is not None:
				query = query.where(UserModel.id.in_(required_ids))

			if filter_by is not None:
				query = query.filter_by(**filter_by)

			found_users = s.scalars(query).all()

		found_users_dto = [UserDTO(**user._asdict(User)) for user in found_users]

		return found_users_dto


	def delete(self, id: Union[str | int]) -> User:
		with Session(self.engine) as s:
			found_user = s.get(UserModel, id)

			s.delete(found_user)

			s.commit()

		return User(**found_user._asdict(User))


	def email_exists(self, email: str) -> bool:
		with Session(self.engine) as s:
			query = (
				select(UserModel.id)
				.filter_by(email=email)
			)

			found_user = s.scalars(query).first()

		return found_user is not None