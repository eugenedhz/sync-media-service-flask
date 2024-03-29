from sqlalchemy import Engine, update, select
from sqlalchemy.orm import Session, defer
from typing import Union, Optional, Any

from src.domain.user import User
from src.interface.repository.user import UserRepoInterface
from src.repository.sqla_models.models import UserModel
from src.usecase.dto import QueryParametersDTO
from src.usecase.user.dto import UserUpdateDTO, UserDTO

from pkg.sqlalchemy.utils import get_first, get_all, formalize_filters


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


	def get_by_id(self, id: int) -> User:
		with Session(self.engine) as s:
			query = (
				select(UserModel)
				.where(UserModel.id == id)
			)

			found_user = get_first(session=s, query=query)

		if found_user is None:
			return None

		return User(**found_user._asdict(User))
			

	def get_by_username(self, username: str) -> User:
		with Session(self.engine) as s:
			query = (
				select(UserModel)
				.where(UserModel.username == username)
			)

			found_user = get_first(session=s, query=query)

		if found_user is None:
			return None

		return User(**found_user._asdict(User))


	def update(self, id: int, update_user_dto: UserUpdateDTO) -> User:
		with Session(self.engine) as s:
			query = (
				update(UserModel)
				.where(UserModel.id == id)
				.values(**update_user_dto)
			)

			s.execute(query)

			s.commit()

			updated_user = s.get(UserModel, id)

		return User(**updated_user._asdict(User))


	def get_all(self, ids: Optional[tuple[int, ...]], query_parameters: QueryParametersDTO) -> list[UserDTO]:
		with Session(self.engine) as s:
			query = (
				select(UserModel)
				.options(defer(UserModel.passwordHash))
			)

			filters = query_parameters.filters

			if ids is not None:
				query = query.where(UserModel.id.in_(ids))

			if filters is not None:
				filters = formalize_filters(filters, UserModel)
				query = query.filter(*filters)

			found_users = get_all(session=s, query=query)

		found_users_dto = [UserDTO(**user._asdict(User)) for user in found_users]

		return found_users_dto


	def delete(self, id: int) -> User:
		with Session(self.engine) as s:
			found_user = s.get(UserModel, id)

			s.delete(found_user)

			s.commit()

		return User(**found_user._asdict(User))


	def field_exists(self, field: dict[str: Any]) -> bool:
		with Session(self.engine) as s:
			query = (
				select(UserModel.id)
				.filter_by(**field)
			)

			found_user = get_first(session=s, query=query)

		return found_user is not None