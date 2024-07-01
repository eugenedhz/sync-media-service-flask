from sqlalchemy import Row
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from typing import Union, Optional, Any
from datetime import datetime

from src.domain.user import User
from src.interface.repository.user import UserRepoInterface
from src.usecase.dto import QueryParametersDTO
from src.usecase.user.dto import (
	UserCreateDTO, UserDTO, UserCheckPasswordDTO, UserUpdateDTO
)

class UserUsecase():
	def __init__(self, repo: UserRepoInterface):
		self.repo = repo


	def create_user(self, user_dto: UserCreateDTO) -> UserDTO:
		password_hash = generate_password_hash(user_dto.password)
		registration_date = int(datetime.now().timestamp())

		new_user = User(
			username = user_dto.username,
			displayName = user_dto.displayName,
			email = user_dto.email,
			passwordHash = password_hash,
			registrationDate = registration_date
		)

		stored_user = self.repo.store(new_user)
		stored_user_dict = stored_user.to_dict()
		del stored_user_dict['passwordHash']

		return UserDTO(**stored_user_dict)


	def check_user_password(self, check_password_dto: UserCheckPasswordDTO) -> bool:
		found_user = self.repo.get_by_username(username=check_password_dto.username)

		password_hash = found_user.passwordHash

		return check_password_hash(password_hash, check_password_dto.password)


	def get_by_username(self, username: str) -> Optional[UserDTO]:
		found_user = self.repo.get_by_username(username=username)

		if found_user is None:
			return None

		found_user_dict = found_user.to_dict()
		del found_user_dict['passwordHash']

		return UserDTO(**found_user_dict)


	def get_by_id(self, id: int) -> Optional[UserDTO]:
		found_user = self.repo.get_by_id(id=id)

		if found_user is None:
			return None

		found_user_dict = found_user.to_dict()
		del found_user_dict['passwordHash']

		return UserDTO(**found_user_dict)


	def get_users(self, query_parameters_dto: QueryParametersDTO) -> list[UserDTO]:
		users = self.repo.get_all(query_parameters_dto)

		return users


	def update_user(self, id: int, update_user_dto: UserUpdateDTO) -> UserDTO:
		if 'password' in update_user_dto:
			update_user_dto['passwordHash'] = generate_password_hash(update_user_dto['password'])
			del update_user_dto['password']

		updated_user = self.repo.update(id, update_user_dto)

		updated_user_dict = updated_user.to_dict()
		del updated_user_dict['passwordHash']

		return UserDTO(**updated_user_dict)


	def delete_user(self, id: int) -> UserDTO:
		deleted_user = self.repo.delete(id=id)

		deleted_user_dict = deleted_user.to_dict()
		del deleted_user_dict['passwordHash']

		return UserDTO(**deleted_user_dict)


	def send_friend_request(self, requesting_user_id: int, receiving_user_id: int) -> UserDTO:
		friend = self.repo.send_friend_request(
			requesting_user_id=requesting_user_id,
			receiving_user_id=receiving_user_id
		)

		friend_dict = friend.to_dict()
		del friend_dict['passwordHash']

		return UserDTO(**friend_dict)


	def delete_friend_request(self, friend_id: int, request: Row) -> UserDTO:
		friend = self.repo.delete_friend_request(
			friend_id=friend_id,
			request=request
		)

		friend_dict = friend.to_dict()
		del friend_dict['passwordHash']

		return UserDTO(**friend_dict)


	def add_friend(self, requesting_user_id: int, receiving_user_id: int, received_request: Row) -> UserDTO:
		friend = self.repo.add_friend(
			requesting_user_id=requesting_user_id,
			receiving_user_id=receiving_user_id,
			received_request=received_request
		)

		friend_dict = friend.to_dict()
		del friend_dict['passwordHash']

		return UserDTO(**friend_dict)


	def delete_friend(self, user_id: int, friend_id: int) -> UserDTO:
		friend = self.repo.delete_friend(user_id=user_id, friend_id=friend_id)

		friend_dict = friend.to_dict()
		del friend_dict['passwordHash']

		return UserDTO(**friend_dict)


	def get_friends(self, user_id: int) -> list[UserDTO]:
		friends = self.repo.get_friends(user_id=user_id)

		return friends


	def get_received_friend_requests(self, user_id: int) -> list[UserDTO]:
		friends = self.repo.get_received_friend_requests(user_id=user_id)

		return friends


	def get_sent_friend_requests(self, user_id: int) -> list[UserDTO]:
		friends = self.repo.get_sent_friend_requests(user_id=user_id)

		return friends


	def is_already_friends(self, user_id: int, friend_id: int) -> bool:
		is_already_friends = self.repo.is_already_friends(user_id=user_id, friend_id=friend_id)

		return is_already_friends


	def has_request(self, requesting_user_id: int, receiving_user_id: int) -> bool | Row:
		has_request = self.repo.has_request(
			requesting_user_id=requesting_user_id,
			receiving_user_id=receiving_user_id
		)

		return has_request


	def is_field_exists(self, name: str, value: str) -> bool:
		is_exists = self.repo.is_field_exists({name: value})

		return is_exists