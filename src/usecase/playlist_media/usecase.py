from typing import Any, Optional

from src.domain.playlist_media import PlaylistMedia
from src.interface.repository.playlist_media import PlaylistMediaRepoInterface
from src.usecase.playlist_media.dto import PlaylistMediaUpdateDTO, PlaylistMediaCreateDTO, PlaylistMediaDTO
from src.usecase.dto import QueryParametersDTO


class PlaylistMediaUsecase():
	def __init__(self, repo: PlaylistMediaRepoInterface):
		self.repo = repo


	def create_playlist_media(self, playlist_media_dto: PlaylistMediaCreateDTO) -> PlaylistMediaDTO:
		new_playlist_media = PlaylistMedia(**playlist_media_dto._asdict())

		return self.repo.store(new_playlist_media)


	def get_playlist_media_by_id(self, id: int) -> Optional[PlaylistMediaDTO]:
		found_playlist_media = self.repo.get_by_id(id)

		if found_playlist_media is None:
			return None

		return found_playlist_media


	def get_playlist_media_by_room_and_media_id(self, room_id: int, media_id: int) -> Optional[PlaylistMediaDTO]:
		found_playlist_media = self.repo.get_by_room_and_media_id(room_id, media_id)

		if found_playlist_media is None:
			return None

		return found_playlist_media


	def get_playlist_medias(self, query_parameters_dto: QueryParametersDTO) -> list[PlaylistMediaDTO]:
		playlist_medias = self.repo.get_all(query_parameters_dto)

		return playlist_medias


	def get_room_playlist_medias(self, room_id: int) -> list[PlaylistMediaDTO]:
		playlist_medias = self.repo.get_room_playlist_medias(room_id)

		return playlist_medias


	def get_playlist_media_by_order(self, room_id: int, order: int) -> PlaylistMediaDTO:
		playlist_media = self.repo.get_by_order(room_id, order)

		return playlist_media


	def update_playlist_media(self, id: int, update_playlist_media_dto: PlaylistMediaUpdateDTO) -> PlaylistMediaDTO:
		playlist_media = self.repo.update(id, update_playlist_media_dto)

		return playlist_media


	def delete_playlist_media(self, id: int) -> PlaylistMediaDTO:
		deleted_playlist_media = self.repo.delete(id)

		return deleted_playlist_media


	def get_max_playlist_order(self, room_id: int) -> Optional[int]:
		return self.repo.get_max_playlist_order(room_id)


	def is_field_exists(self, name: str, value: Any) -> bool:
		is_exists = self.repo.is_field_exists({name: value})

		return is_exists
