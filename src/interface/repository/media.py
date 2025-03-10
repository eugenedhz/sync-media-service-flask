from abc import ABC, abstractmethod

from typing import Any

from src.usecase.dto import QueryParametersDTO
from src.usecase.media.dto import MediaUpdateDTO, MediaDTO
from src.domain.media import Media


class MediaRepoInterface(ABC):
    @abstractmethod
    def store(self, media: Media) -> Media:
        raise NotImplementedError


    @abstractmethod
    def get_by_id(self, id: int) -> Media:
        raise NotImplementedError


    @abstractmethod
    def update(self, id: int, update_media_dto: MediaUpdateDTO) -> Media:
        raise NotImplementedError


    @abstractmethod
    def get_all(self, query_parameters_dto: QueryParametersDTO, genre_ids: list[int]) -> list[MediaDTO]:
        raise NotImplementedError


    @abstractmethod
    def delete(self, id: int) -> Media:
        raise NotImplementedError


    @abstractmethod
    def is_field_exists(self, field: dict[str: Any]) -> bool:
        raise NotImplementedError

