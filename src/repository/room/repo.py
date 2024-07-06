from sqlalchemy import Engine, update, select
from sqlalchemy.orm import Session
from typing import Any, Optional

from src.domain.room import Room
from src.interface.repository.room import RoomRepoInterface
from src.repository.sqla_models.models import RoomModel, UserModel
from src.usecase.dto import QueryParametersDTO
from src.usecase.room.dto import RoomDTO, RoomUpdateDTO 

from pkg.sqlalchemy.utils import get_first, get_all, formalize_filters


class RoomRepo(RoomRepoInterface):
    def __init__(self, engine: Engine):
        self.engine = engine


    def store(self, room: Room) -> Room:
        with Session(self.engine) as s:
            new_room = RoomModel(**room.to_dict())

            s.add(new_room)

            s.commit()

            s.refresh(new_room)

        return Room(**new_room._asdict(Room))


    def get_by_id(self, id: int) -> Optional[Room]:
        with Session(self.engine) as s:
            query = (
                select(RoomModel)
                .where(RoomModel.id == id)
            )

            found_room = get_first(session=s, query=query)

        if found_room is None:
            return None

        return Room(**found_room._asdict(Room))


    def get_by_name(self, name: str) -> Optional[Room]:
        with Session(self.engine) as s:
            query = (
                select(RoomModel)
                .where(RoomModel.name == name)
            )

            found_room = get_first(session=s, query=query)

        if found_room is None:
            return None

        return Room(**found_room._asdict(Room))


    def update(self, id: int, update_room_dto: RoomUpdateDTO) -> Room:
        with Session(self.engine) as s:
            query = (
                update(RoomModel)
                .where(RoomModel.id == id)
                .values(**update_room_dto)
            )

            s.execute(query)

            s.commit()

            updated_room = s.get(RoomModel, id)

        return Room(**updated_room._asdict(Room))


    def get_all(self, query_parameters: QueryParametersDTO) -> list[RoomDTO]:
        with Session(self.engine) as s:
            query = (
                select(RoomModel)
            )

            filters = query_parameters.filters
            limit, offset = query_parameters_dto.limit, query_parameters_dto.offset 

            if filters is not None:
                filters = formalize_filters(filters, RoomModel)
                query = query.filter(*filters)

            if limit and offset:
                query = query.limit(limit).offset(limit*offset)

            found_rooms = get_all(session=s, query=query)

        found_rooms_dto = [RoomDTO(**room._asdict(Room)) for room in found_rooms]

        return found_rooms_dto


    def get_creator_rooms(self, user_id: int) -> list[RoomDTO]:
        with Session(self.engine) as s:
            query = (
                select(UserModel)
                .where(UserModel.id == user_id)
            )

            creator = get_first(session=s, query=query)
            rooms = creator.createdRooms

        rooms_dto = [RoomDTO(**room._asdict(Room)) for room in rooms]

        return rooms_dto


    def delete(self, id: int) -> Room:
        with Session(self.engine) as s:
            found_room = s.get(RoomModel, id)

            s.delete(found_room)

            s.commit()

        return Room(**found_room._asdict(Room))


    def is_field_exists(self, field: dict[str: Any]) -> bool:
        with Session(self.engine) as s:
            query = (
                select(RoomModel.id)
                .filter_by(**field)
            )

            found_room = get_first(session=s, query=query)

        return found_room is not None
