from abc import ABC, abstractmethod

from typing import Any

from src.domain.room import Room
from src.domain.user import User
from src.usecase.dto import QueryParametersDTO
from src.usecase.room.dto import RoomUpdateDTO


class RoomRepoInterface(ABC):
    @abstractmethod
    def store(self, room: Room) -> Room:
        raise NotImplementedError


    @abstractmethod
    def get_by_id(self, id: int) -> Room:
        raise NotImplementedError


    @abstractmethod
    def get_by_name(self, name: str) -> Room:
        raise NotImplementedError


    @abstractmethod
    def update(self, id: int, update_room_dto: RoomUpdateDTO) -> Room:
        raise NotImplementedError


    @abstractmethod
    def get_all(self, query_parameters_dto: QueryParametersDTO) -> list[RoomDTO]:
        raise NotImplementedError


    @abstractmethod
    def delete(self, id: int) -> Room:
        raise NotImplementedError

    
    @abstractmethod
    def get_creator(self, id: int) -> User:
        raise NotImplementedError

    
    @abstractmethod
    def is_field_exists(self, field: dict[str: Any]) -> bool:
        raise NotImplementedError
