from sqlalchemy import Engine, update, select
from sqlalchemy.orm import Session
from typing import Any, Optional

from src.domain.media_video import MediaVideo
from src.interface.repository.media_video import MediaVideoRepoInterface
from src.repository.sqla_models.models import VideoModel, MediaModel
from src.usecase.dto import QueryParametersDTO
from src.usecase.media_video.dto import MediaVideoDTO, MediaVideoUpdateDTO 

from pkg.sqlalchemy.utils import get_first, get_all, formalize_filters


class MediaVideoRepo(MediaVideoRepoInterface):
    def __init__(self, engine: Engine):
        self.engine = engine


    def store(self, media_video: MediaVideo) -> MediaVideo:
        with Session(self.engine) as s:
            new_video = VideoModel(**media_video.to_dict())

            s.add(new_video)

            s.commit()

            s.refresh(new_video)

        return MediaVideo(**new_video._asdict(MediaVideo))


    def get_by_id(self, id: int) -> Optional[MediaVideo]:
        with Session(self.engine) as s:
            query = (
                select(VideoModel)
                .where(VideoModel.id == id)
            )

            found_video = get_first(session=s, query=query)

        if found_video is None:
            return None

        return MediaVideo(**found_video._asdict(MediaVideo))


    def update(self, id: int, update_video_dto: MediaVideoUpdateDTO) -> MediaVideo:
        with Session(self.engine) as s:
            query = (
                update(VideoModel)
                .where(VideoModel.id == id)
                .values(**update_video_dto)
            )

            s.execute(query)

            s.commit()

            updated_video = s.get(VideoModel, id)

        return MediaVideo(**updated_video._asdict(MediaVideo))


    def get_all(self, query_parameters_dto: QueryParametersDTO) -> list[MediaVideoDTO]:
        with Session(self.engine) as s:
            query = (
                select(VideoModel)
            )

            filters = query_parameters_dto.filters
            limit, offset = query_parameters_dto.limit, query_parameters_dto.offset 

            if filters is not None:
                filters = formalize_filters(filters, VideoModel)
                query = query.filter(*filters)

            if limit and offset:
                query = query.limit(limit).offset(limit*offset)

            found_videos = get_all(session=s, query=query)

        found_videos_dto = [MediaVideoDTO(**video._asdict(MediaVideo)) for video in found_videos]

        return found_videos_dto


    def get_media_videos(self, media_id: int) -> list[MediaVideoDTO]:
        with Session(self.engine) as s:
            query = (
                select(MediaModel)
                .where(MediaModel.id == media_id)
            )

            media = get_first(session=s, query=query)
            videos = media.videos

        videos_dto = [MediaVideoDTO(**video._asdict(MediaVideo)) for video in videos]

        return videos_dto


    def delete(self, id: int) -> MediaVideo:
        with Session(self.engine) as s:
            found_video = s.get(VideoModel, id)

            s.delete(found_video)

            s.commit()

        return MediaVideo(**found_video._asdict(MediaVideo))


    def is_field_exists(self, field: dict[str: Any]) -> bool:
        with Session(self.engine) as s:
            query = (
                select(VideoModel.id)
                .filter_by(**field)
            )

            found_video = get_first(session=s, query=query)

        return found_video is not None
