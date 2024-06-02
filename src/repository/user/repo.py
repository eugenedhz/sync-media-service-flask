from datetime import date

from sqlalchemy import Engine, update, select, delete
from sqlalchemy.orm import Session, defer
from typing import Union, Optional, Any

from src.domain.user import User
from src.interface.repository.user import UserRepoInterface
from src.repository.sqla_models.models import UserModel, FriendshipRequestModel, FriendshipModel
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


	def _send_friend_request(self, requesting_user_id: int, receiving_user_id: int):
		with Session(self.engine) as s:
			# Создаем новый запрос на дружбу
			new_request = FriendshipRequestModel(
				requesting_user_id=requesting_user_id,
				receiving_user_id=receiving_user_id
			)
			s.add(new_request)
			s.commit()


	def add_friend(self, requesting_user_id: int, receiving_user_id: int) -> User:
		with Session(self.engine) as s:
			# Проверяем, существует ли обратный запрос на дружбу
			friendship_request = s.query(FriendshipRequestModel).filter_by(
				requesting_user_id=receiving_user_id,
				receiving_user_id=requesting_user_id
			).first()

			if not friendship_request:
				self._send_friend_request(
					requesting_user_id=requesting_user_id,
					receiving_user_id=receiving_user_id
				)

			else:

				# Создаем запись в таблице дружбы
				friendship = FriendshipModel(
					user_1=requesting_user_id,
					user_2=receiving_user_id
				)
				s.add(friendship)

				# Удаляем запрос на дружбу
				s.delete(friendship_request)
				s.commit()

		friend = s.get(UserModel, receiving_user_id)

		return User(**friend._asdict(User))


	def delete_friend(self, user_id: int, friend_id: int) -> User:
		with Session(self.engine) as s:
			friendship = s.query(FriendshipModel).filter(
				((FriendshipModel.user_1 == user_id) & (FriendshipModel.user_2 == friend_id)) |
				((FriendshipModel.user_1 == friend_id) & (FriendshipModel.user_2 == user_id))
			).one()

			s.delete(friendship)
			s.commit()

			deleted_friend = s.get(UserModel, friend_id)

			return User(**deleted_friend._asdict(User))


	def get_friends(self, user_id: int) -> list[UserDTO]:
		with Session(self.engine) as s:
			friendships_as_user_1 = s.query(FriendshipModel).filter_by(user_1=user_id).all()
			friendships_as_user_2 = s.query(FriendshipModel).filter_by(user_2=user_id).all()

			friend_ids = set([friendship.user_2 for friendship in friendships_as_user_1] +
							 [friendship.user_1 for friendship in friendships_as_user_2])

			friends = s.query(UserModel).filter(UserModel.id.in_(friend_ids)).options(defer(UserModel.passwordHash)).all()

			friends_dto = [UserDTO(**friend._asdict(User)) for friend in friends]

			return friends_dto


	def get_received_friend_requests(self, user_id: int) -> list[UserDTO]:
		with Session(self.engine) as s:
			requests_received = s.query(FriendshipRequestModel).filter_by(receiving_user_id=user_id, is_rejected=False).all()

			requesting_user_ids = [request.requesting_user_id for request in requests_received]

			requesting_users = s.query(UserModel).filter(UserModel.id.in_(requesting_user_ids)).options(defer(UserModel.passwordHash)).all()

			found_users_dto = [UserDTO(**user._asdict(User)) for user in requesting_users]

			return found_users_dto


	def get_sent_friend_requests(self, user_id: int) -> list[UserDTO]:
		with Session(self.engine) as s:
			requests_sent = s.query(FriendshipRequestModel).filter_by(requesting_user_id=user_id).all()

			receiving_user_ids = [request.receiving_user_id for request in requests_sent]

			receiving_users = s.query(UserModel).filter(UserModel.id.in_(
				receiving_user_ids)).options(defer(UserModel.passwordHash)).all()

			found_users_dto = [UserDTO(**user._asdict(User)) for user in receiving_users]

			return found_users_dto


	def delete_sent_friend_request(self, requesting_user_id: int, receiving_user_id: int) -> User:
		with Session(self.engine) as s:
			sent_request = s.query(FriendshipRequestModel).filter_by(
				requesting_user_id=requesting_user_id, receiving_user_id=receiving_user_id).first()

			s.delete(sent_request)
			s.commit()

		canceled_friend = s.get(UserModel, receiving_user_id)

		return User(**canceled_friend._asdict(User))


	def reject_friend_request(self, user_id: int, requesting_user_id: int) -> User:
		with Session(self.engine) as s:
			request = s.query(FriendshipRequestModel).filter_by(
				receiving_user_id=user_id,
				requesting_user_id=requesting_user_id,
				is_rejected=False
			).one()

			request.is_rejected = True
			s.commit()

		rejected_user = s.get(UserModel, requesting_user_id)

		return User(**rejected_user._asdict(User))


	def is_field_exists(self, field: dict[str: Any]) -> bool:
		with Session(self.engine) as s:
			query = (
				select(UserModel.id)
				.filter_by(**field)
			)

			found_user = get_first(session=s, query=query)

		return found_user is not None