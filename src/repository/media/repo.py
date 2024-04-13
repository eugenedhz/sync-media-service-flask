from sqlalchemy import Engine, update, select
from sqlalchemy.orm import Session
from typing import Any

from src.domain.media import Media
from src.interface.repository.media import MediaRepoInterface
from src.repository.sqla_models.models import MediaModel
from src.usecase.dto import QueryParametersDTO
from src.usecase.media.dto import MediaUpdateDTO, MediaDTO, MediaCreateDTO

from pkg.sqlalchemy.utils import get_first, get_all, formalize_filters


class MediaRepo(MediaRepoInterface):
    def __init__(self, engine: Engine):
        self.engine = engine


    def store(self, media: Media) -> Media:
        with Session(self.engine) as s:
            new_media = MediaModel(**(media.to_dict()))

            s.add(new_media)

            s.commit()

            s.refresh(new_media)

        return Media(**new_media._asdict(Media))


    def get_by_id(self, id: int) -> Media:
        with Session(self.engine) as s:
            query = (
                select(MediaModel)
                .where(MediaModel.id == id)
            )

            found_media = get_first(session=s, query=query)

        if found_media is None:
            return None

        return Media(**found_media._asdict(Media))


    def update(self, id: int, update_media_dto: MediaUpdateDTO) -> Media:
        with Session(self.engine) as s:
            query = (
                update(MediaModel)
                .where(MediaModel.id == id)
                .values(**update_media_dto)
            )

            s.execute(query)

            s.commit()

            updated_media = s.get(MediaModel, id)

        return Media(**updated_media._asdict(Media))


    def get_all(self, query_parameters: QueryParametersDTO) -> list[MediaDTO]:
        with Session(self.engine) as s:
            query = (
                select(MediaModel)
            )

            filters = query_parameters.filters

            if filters is not None:
                filters = formalize_filters(filters, MediaModel)
                query = query.filter(*filters)

            found_medias = get_all(session=s, query=query)

        found_medias_dto = [MediaDTO(**media._asdict(Media)) for media in found_medias]

        return found_medias_dto


    def delete(self, id: int) -> Media:
        with Session(self.engine) as s:
            found_media = s.get(MediaModel, id)

            s.delete(found_media)

            s.commit()

        return Media(**found_media._asdict(Media))


    def field_exists(self, field: dict[str: Any]) -> bool:
        with Session(self.engine) as s:
            query = (
                select(MediaModel)
                .filter_by(**field)
            )

            found_media = get_first(session=s, query=query)

        return found_media is not None