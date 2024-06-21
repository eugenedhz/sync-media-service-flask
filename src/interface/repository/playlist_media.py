from abc import ABC, abstractmethod

from typing import Any

from src.usecase.dto import QueryParametersDTO
from src.usecase.playlist_media.dto import PlaylistMediaUpdateDTO, PlaylistMediaDTO
from src.domain.playlist_media import PlaylistMedia


class PlaylistMediaRepoInterface(ABC):
    @abstractmethod
    def store(self, playlist_media: PlaylistMedia) -> PlaylistMediaDTO:
        raise NotImplementedError


    @abstractmethod
    def get_max_playlist_order(self) -> Optional[int]:
        raise NotImplementedError


    @abstractmethod
    def get_by_id(self, id: int) -> PlaylistMediaDTO:
        raise NotImplementedError


    @abstractmethod
    def get_by_room_and_media_id(self, room_id: int, media_id: int) -> PlaylistMediaDTO:
        raise NotImplementedError


    @abstractmethod
    def update(self, id: int, update_playlist_media_dto: PlaylistMediaUpdateDTO) -> PlaylistMediaDTO:
        raise NotImplementedError


    @abstractmethod
    def get_all(self, query_parameters_dto: QueryParametersDTO) -> list[PlaylistMediaDTO]:
        raise NotImplementedError


    @abstractmethod
    def get_room_playlist_medias(self, room_id: int) -> list[PlaylistMediaDTO]:
        raise NotImplementedError


    @abstractmethod
    def delete(self, id: int) -> PlaylistMediaDTO:
        raise NotImplementedError


    @abstractmethod
    def is_field_exists(self, field: dict[str: Any]) -> bool:
        raise NotImplementedError

