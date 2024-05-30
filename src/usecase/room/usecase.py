from typing import Any, Optional

from src.domain.room import Room
from src.interface.repository.room import RoomRepoInterface
from src.usecase.dto import QueryParametersDTO
from src.usecase.room.dto import RoomDTO, RoomCreateDTO, RoomUpdateDTO 


class RoomUsecase():
	def __init__(self, repo: RoomRepoInterface):
		self.repo = repo


	def create_room(self, room_dto: RoomCreateDTO) -> RoomDTO:
		new_room = Room(**room_dto._asdict())
		stored_room = self.repo.store(new_room)

		return RoomDTO(**stored_room.to_dict())


	def get_room_by_id(self, id: int) -> Optional[RoomDTO]:
		found_room = self.repo.get_by_id(id)

		if found_room is None:
			return None

		return RoomDTO(**found_room.to_dict())


	def get_room_by_name(self, name: str) -> Optional[RoomDTO]:
		found_room = self.repo.get_by_name(id)

		if found_room is None:
			return None

		return RoomDTO(**found_room.to_dict())


	def get_rooms(self, query_parameters_dto: QueryParametersDTO) -> list[RoomDTO]:
		rooms = self.repo.get_all(query_parameters_dto)

		return rooms


	def get_creator_rooms(self, user_id: int) -> list[RoomDTO]:
		rooms = self.repo.get_creator_rooms(user_id)

		return rooms


	def update_room(self, id: int, update_room_dto: RoomUpdateDTO) -> RoomDTO:
		updated_room = self.repo.update(id, update_room_dto)

		return RoomDTO(**updated_room.to_dict())


	def delete_room(self, id: int) -> RoomDTO:
		deleted_room = self.repo.delete(id=id)

		return RoomDTO(**deleted_room.to_dict())


	def is_field_exists(self, name: str, value: Any) -> bool:
		is_exists = self.repo.is_field_exists({name: value})

		return is_exists
