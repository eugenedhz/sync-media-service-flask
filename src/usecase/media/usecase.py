from typing import Optional

from src.domain.media import Media
from src.interface.repository.media import MediaRepoInterface
from src.usecase.dto import QueryParametersDTO
from src.usecase.media.dto import (
	MediaCreateDTO, MediaDTO, MediaUpdateDTO
)


class MediaUsecase():

	def __init__(self, repo: MediaRepoInterface):
		self.repo = repo

	def create_media(self, media_dto: MediaCreateDTO) -> MediaDTO:

		new_media = Media(
			name = media_dto.name,
			description = media_dto.description,
			thumbnail = media_dto.thumbnail,
			preview = media_dto.preview,
		)

		stored_media = self.repo.store(new_media)
		stored_media_dict = stored_media.to_dict()

		return MediaDTO(**stored_media_dict)

	def get_by_name(self, name: str) -> Optional[MediaDTO]:

		found_media = self.repo.get_by_name(name=name)

		if found_media is None:
			return None

		found_media_dict = found_media.to_dict()

		return MediaDTO(**found_media_dict)

	def get_by_id(self, id: int) -> Optional[MediaDTO]:

		found_media = self.repo.get_by_id(id=id)

		if found_media is None:
			return None

		found_media_dict = found_media.to_dict()

		return MediaDTO(**found_media_dict)

	def get_medias(self, ids: tuple[int, ...], query_parameters: QueryParametersDTO) -> list[MediaDTO]:
		medias = self.repo.get_all(ids, query_parameters)

		return medias

	def update_media(self, id: int, update_media_dto: MediaUpdateDTO) -> MediaDTO:
		updated_media = self.repo.update(id, update_media_dto)

		updated_media_dict = updated_media.to_dict()

		return MediaDTO(**updated_media_dict)

	def delete_media(self, id: int) -> MediaDTO:
		deleted_media = self.repo.delete(id=id)

		deleted_media_dict = deleted_media.to_dict()

		return MediaDTO(**deleted_media_dict)

	def field_exists(self, name: str, value: str) -> bool:
		field = dict()
		field[name] = value

		exists = self.repo.field_exists(field)

		return exists
