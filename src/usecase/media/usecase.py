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
		new_media = Media(**media_dto._asdict())

		stored_media = self.repo.store(new_media)

		return MediaDTO(**stored_media.to_dict())


	def get_by_id(self, id: int) -> Optional[MediaDTO]:
		found_media = self.repo.get_by_id(id=id)

		if found_media is None:
			return None

		return MediaDTO(**found_media.to_dict())


	def get_medias(self, query_parameters_dto: QueryParametersDTO) -> list[MediaDTO]:
		medias = self.repo.get_all(query_parameters_dto)

		return medias


	def update_media(self, id: int, update_media_dto: MediaUpdateDTO) -> MediaDTO:
		updated_media = self.repo.update(id, update_media_dto)

		return MediaDTO(**updated_media.to_dict())


	def delete_media(self, id: int) -> MediaDTO:
		deleted_media = self.repo.delete(id=id)

		return MediaDTO(**deleted_media.to_dict())


	def is_field_exists(self, name: str, value: str) -> bool:
		is_exists = self.repo.is_field_exists({name: value})

		return is_exists
