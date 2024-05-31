from abc import ABC, abstractmethod

from typing import Any

from src.domain.media_video import MediaVideo
from src.usecase.dto import QueryParametersDTO
from src.usecase.media_video.dto import MediaVideoUpdateDTO, MediaVideoDTO


class MediaVideoRepoInterface(ABC):
    @abstractmethod
    def store(self, media_video: MediaVideo) -> MediaVideo:
        raise NotImplementedError


    @abstractmethod
    def get_by_id(self, id: int) -> MediaVideo:
        raise NotImplementedError


    @abstractmethod
    def update(self, id: int, update_video_dto: MediaVideoUpdateDTO) -> MediaVideo:
        raise NotImplementedError


    @abstractmethod
    def get_all(self, query_parameters_dto: QueryParametersDTO) -> list[MediaVideoDTO]:
        raise NotImplementedError


    @abstractmethod
    def get_media_videos(self, media_id: int) -> list[MediaVideoDTO]:
        raise NotImplementedError


    @abstractmethod
    def delete(self, id: int) -> MediaVideo:
        raise NotImplementedError

    
    @abstractmethod
    def is_field_exists(self, field: dict[str: Any]) -> bool:
        raise NotImplementedError
