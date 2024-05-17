from datetime import date

from sqlalchemy import Engine, update, select, delete
from sqlalchemy.orm import Session, defer
from typing import Union, Optional, Any

from src.domain.user import User
from src.interface.repository.user import UserRepoInterface
from src.repository.sqla_models.models import UserModel, RelationsModel
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


	def get_all(self, query_parameters_dto: QueryParametersDTO) -> list[UserDTO]:
		with Session(self.engine) as s:
			query = (
				select(UserModel)
				.options(defer(UserModel.passwordHash))
			)

			filters = query_parameters_dto.filters

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


	def _get_relation(self, session: Session, user_id: int, friend_id: int):
		return session.query(RelationsModel).filter(
			RelationsModel.user_1 == user_id,
			RelationsModel.user_2 == friend_id,
			RelationsModel.state.in_(['pending', 'friends'])
		).first()


	def _update_relation_to_friends(self, session: Session, user_id: int, friend_id: int):
		stmt = (
			update(RelationsModel)
			.where(RelationsModel.user_1 == user_id, RelationsModel.user_2 == friend_id)
			.values(state='friends')
		)
		session.execute(stmt)


	def _get_friends_query(self, session: Session, user_id: int):
		return session.query(UserModel).join(
			RelationsModel, RelationsModel.user_2 == UserModel.id
		).filter(
			RelationsModel.user_1 == user_id,
			RelationsModel.state == 'friends'
		).options(defer(UserModel.passwordHash))


	def _delete_relation(self, session: Session, user_id: int, friend_id: int):
		stmt = (
			delete(RelationsModel)
			.where(RelationsModel.user_1 == user_id, RelationsModel.user_2 == friend_id)
		)
		session.execute(stmt)


	def _update_relation_to_pending(self, session: Session, user_id: int, friend_id: int):
		stmt = (
			update(RelationsModel)
			.where(RelationsModel.user_1 == user_id, RelationsModel.user_2 == friend_id)
			.values(state='pending')
		)
		session.execute(stmt)


	def get_friends(self, id: int) -> list[UserDTO]:
		with Session(self.engine) as s:
			friends = self._get_friends_query(s, id).all()

			return [UserDTO(**user._asdict(User)) for user in friends]


	def add_friend(self, id: int, friend_id: int):
		with Session(self.engine) as s:
			if id == friend_id:
				raise ValueError("Users cannot add themselves as a friend")

			relation = self._get_relation(s, id, friend_id)

			if not relation:
				reverse_relation = self._get_relation(s, friend_id, id)

				if reverse_relation and reverse_relation.state == 'pending':
					self._update_relation_to_friends(s, friend_id, id)
					new_relation = RelationsModel(user_1=id, user_2=friend_id, state='friends',
												  created=date.today())
				else:
					new_relation = RelationsModel(user_1=id, user_2=friend_id, state='pending',
												  created=date.today())

				s.add(new_relation)
				s.commit()

			return self.get_by_id(friend_id)


	def delete_friend(self, id: int, friend_id: int) -> User:
		with Session(self.engine) as s:

			relation = self._get_relation(s, id, friend_id)
			reverse_relation = self._get_relation(s, friend_id, id)

			if relation:
				self._delete_relation(s, id, friend_id)
			if reverse_relation and reverse_relation.state == 'friends':
				self._update_relation_to_pending(s, friend_id, id)

			s.commit()

			return self.get_by_id(friend_id)


	def is_field_exists(self, field: dict[str: Any]) -> bool:
		with Session(self.engine) as s:
			query = (
				select(UserModel.id)
				.filter_by(**field)
			)

			found_user = get_first(session=s, query=query)

		return found_user is not None