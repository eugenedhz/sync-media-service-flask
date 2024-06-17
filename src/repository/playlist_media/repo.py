from sqlalchemy import Engine, update, select, func, asc
from sqlalchemy.orm import Session
from typing import Any, Optional

from src.domain.playlist_media import PlaylistMedia
from src.repository.sqla_models.models import PlaylistMediaModel
from src.usecase.playlist_media.dto import PlaylistMediaUpdateDTO, PlaylistMediaDTO
from src.usecase.dto import QueryParametersDTO

from pkg.sqlalchemy.utils import get_first, get_all, formalize_filters


class PlaylistMediaRepo(PlaylistMediaRepoInterface):
    def __init__(self, engine: Engine):
        self.engine = engine


    def get_max_playlist_order(self) -> Optional[int]:
        with Session(self.engine) as s:
            query = (
                select(PlaylistMediaModel, func.max(PlaylistMediaModel.order))
            )

            last_playlist_media = get_first(session=s, query=query)
            if last_playlist_media:
                return last_playlist_media.order

            return None


    def store(self, playlist_media: PlaylistMedia) -> PlaylistMediaDTO:
        with Session(self.engine) as s:
            max_order = self.get_max_playlist_order()
            new_order = 1

            if max_order:
                new_order = max_order + 1

            new_playlist_media = ParticipantModel(**playlist_media.to_dict())
            new_playlist_media.order = new_order

            s.add(new_playlist_media)

            s.commit()

            s.refresh(new_playlist_media)
            s.refresh(new_playlist_media.media)

        name = new_playlist_media.name
        thumbnail = new_playlist_media.thumbnail
        return PlaylistMediaDTO(**new_playlist_media._asdict(PlaylistMedia), name=name, thumbnail=thumbnail)


    def get_by_id(self, id: int) -> Optional[PlaylistMediaDTO]:
        with Session(self.engine) as s:
            query = (
                select(PlaylistMediaModel)
                .where(PlaylistMediaModel.id == id)
            )

            playlist_media = get_first(session=s, query=query)
            s.refresh(playlist_media.media)

        if playlist_media is None:
            return None

        name = playlist_media.name
        thumbnail = playlist_media.thumbnail
        return PlaylistMediaDTO(**playlist_media._asdict(PlaylistMedia), name=name, thumbnail=thumbnail)


    def get_by_room_and_media_id(self, room_id: int, media_id: int) -> Optional[PlaylistMediaDTO]:
        with Session(self.engine) as s:
            query = (
                select(PlaylistMediaModel)
                .where(PlaylistMediaModel.roomId == room_id)
                .where(PlaylistMediaModel.mediaId == media_id)
            )

            playlist_media = get_first(session=s, query=query)
            s.refresh(playlist_media.media)

        if playlist_media is None:
            return None

        name = playlist_media.name
        thumbnail = playlist_media.thumbnail
        return PlaylistMediaDTO(**playlist_media._asdict(PlaylistMedia), name=name, thumbnail=thumbnail)


    # обновление порядка остальных медиа, при кейсе обновления или удаления медиа в плейлисте
    def _update_orders(self, session: Session, current_order: int, new_order: Optional[int] = None) -> None:
        query = update(PlaylistMediaModel)

        # кейс удаления
        if new_order is None:
            query = (
                query
                .filter(PlaylistMediaModel.order > current_order)
                .values(order=PlaylistMediaModel.order - 1)
            )

            s.execute(query)
            return

        if current_order < new_order:
            query = (
                query
                .filter(PlaylistMediaModel.order > current_order, PlaylistMediaModel.order <= new_order)
                .values(order=PlaylistMediaModel.order - 1)
            )
        else:
            query = (
                query
                .filter(PlaylistMediaModel.order < current_order, PlaylistMediaModel.order >= new_order)
                .values(order=PlaylistMediaModel.order + 1)
            )

        s.execute(query)


    def update(self, id: int, update_playlist_media_dto: PlaylistMediaUpdateDTO) -> PlaylistMediaDTO:
        with Session(self.engine) as s:
            playlist_media = s.get(PlaylistMediaModel, id)

            if 'order' in update_playlist_media_dto:
                current_order = playlist_media.order
                new_order = update_playlist_media_dto['order']
                self._update_orders(s, current_order, new_order)

            query = (
                update(PlaylistMediaModel)
                .where(PlaylistMediaModel.id == id)
                .values(**update_playlist_media_dto)
            )

            s.execute(query)  
            s.commit()

            s.refresh(playlist_media)
            s.refresh(playlist_media.media)

        name = playlist_media.name
        thumbnail = playlist_media.thumbnail
        return PlaylistMediaDTO(**playlist_media._asdict(PlaylistMedia), name=name, thumbnail=thumbnail)           


    def get_all(self, query_parameters_dto: QueryParametersDTO) -> list[PlaylistMediaDTO]:
        with Session(self.engine) as s:
            query = (
                select(PlaylistMediaModel)
            )

            filters = query_parameters.filters

            if filters is not None:
                filters = formalize_filters(filters, PlaylistMediaModel)
                query = query.filter(*filters)

            query = query.order_by(asc(PlaylistMediaModel.order))

            found_playlist_media = get_all(session=s, query=query)
            
            playlist_media_dto = [
                PlaylistMediaDTO(**playlist_media._asdict(PlaylistMedia), name=playlist_media.name, thumbnail=playlist_media.thumbnail)
                for playlist_media in found_playlist_media
            ]

        return playlist_media_dto


    def get_room_playlist_medias(self, room_id: int) -> list[PlaylistMediaDTO]:
        with Session(self.engine) as s:
            query = (
                select(PlaylistMediaModel)
                .where(PlaylistMediaModel.roomId == room_id)
                .order_by(asc(PlaylistMediaModel.order))
            )

            found_playlist_media = get_all(session=s, query=query)
            
            playlist_media_dto = [
                PlaylistMediaDTO(**playlist_media._asdict(PlaylistMedia), name=playlist_media.name, thumbnail=playlist_media.thumbnail)
                for playlist_media in found_playlist_media
            ]

        return playlist_media_dto


    def delete(self, id: int) -> PlaylistMediaDTO:
        with Session(self.engine) as s:
            playlist_media = s.get(PlaylistMediaModel, id)
            current_order = playlist_media.order

            self._update_orders(session=s, current_order)

            name = playlist_media.name
            thumbnail = playlist_media.thumbnail

            s.delete(playlist_media)

            s.commit()

        return PlaylistMediaDTO(**playlist_media._asdict(PlaylistMedia), name=name, thumbnail=thumbnail)


    def is_field_exists(self, field: dict[str: Any]) -> bool:
        with Session(self.engine) as s:
            query = (
                select(PlaylistMediaModel.id)
                .filter_by(**field)
            )

            playlist_media = get_first(session=s, query=query)

        return playlist_media is not None
