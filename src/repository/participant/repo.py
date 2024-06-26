from sqlalchemy import Engine, update, select
from sqlalchemy.orm import Session
from typing import Optional, Any

from src.domain.participant import Participant
from src.interface.repository.participant import ParticipantRepoInterface
from src.repository.sqla_models.models import ParticipantModel, UserModel, RoomModel
from src.usecase.dto import QueryParametersDTO
from src.usecase.participant.dto import ParticipantDTO

from pkg.sqlalchemy.utils import get_first, get_all, formalize_filters


class ParticipantRepo(ParticipantRepoInterface):
    def __init__(self, engine: Engine):
        self.engine = engine


    def store(self, participant: Participant) -> ParticipantDTO:
        with Session(self.engine) as s:
            new_participant = ParticipantModel(**participant.to_dict())

            s.add(new_participant)

            s.commit()

            s.refresh(new_participant)
            s.refresh(new_participant.user)

        name = new_participant.name
        avatar = new_participant.avatar
        return ParticipantDTO(**new_participant._asdict(Participant), name=name, avatar=avatar)


    def get_by_id(self, id: int) -> Optional[ParticipantDTO]:
        with Session(self.engine) as s:
            query = (
                select(ParticipantModel)
                .where(ParticipantModel.id == id)
            )

            found_participant = get_first(session=s, query=query)
            if found_participant is None:
                return None

            s.refresh(found_participant.user)

        name = found_participant.name
        avatar = found_participant.avatar
        return ParticipantDTO(**found_participant._asdict(Participant), name=name, avatar=avatar)


    def get_by_user_and_room_id(self, user_id: int, room_id: int) -> Optional[ParticipantDTO]:
        with Session(self.engine) as s:
            query = (
                select(ParticipantModel)
                .where(ParticipantModel.userId == user_id)
                .where(ParticipantModel.roomId == room_id)
            )

            found_participant = get_first(session=s, query=query)
            if found_participant is None:
                return None

            s.refresh(found_participant.user)

        name = found_participant.name
        avatar = found_participant.avatar
        return ParticipantDTO(**found_participant._asdict(Participant), name=name, avatar=avatar)


    def get_all(self, query_parameters: QueryParametersDTO) -> list[ParticipantDTO]:
        with Session(self.engine) as s:
            query = (
                select(ParticipantModel)
            )

            filters = query_parameters.filters

            if filters is not None:
                filters = formalize_filters(filters, ParticipantModel)
                query = query.filter(*filters)

            found_participants = get_all(session=s, query=query)
            
            participants_dto = [
                ParticipantDTO(**participant._asdict(Participant), name=participant.name, avatar=participant.avatar)
                for participant in found_participants
            ]

        return participants_dto


    def get_room_participants(self, room_id: int) -> list[ParticipantDTO]:
        with Session(self.engine) as s:
            query = (
                select(ParticipantModel)
                .where(ParticipantModel.roomId == room_id)
            )

            found_participants = get_all(session=s, query=query)
            
            participants_dto = [
                ParticipantDTO(**participant._asdict(Participant), name=participant.name, avatar=participant.avatar)
                for participant in found_participants
            ]

        return participants_dto


    def delete(self, id: int) -> ParticipantDTO:
        with Session(self.engine) as s:
            found_participant = s.get(ParticipantModel, id)
            name = found_participant.name
            avatar = found_participant.avatar

            s.delete(found_participant)

            s.commit()

        return ParticipantDTO(**found_participant._asdict(Participant), name=name, avatar=avatar)


    def is_field_exists(self, field: dict[str: Any]) -> bool:
        with Session(self.engine) as s:
            query = (
                select(ParticipantModel.id)
                .filter_by(**field)
            )

            found_participant = get_first(session=s, query=query)

        return found_participant is not None
