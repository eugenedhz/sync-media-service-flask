from typing import Any, Optional

from src.domain.media_video import MediaVideo
from src.interface.repository.media_video import MediaVideoRepoInterface
from src.usecase.dto import QueryParametersDTO
from src.usecase.media_video.dto import MediaVideoDTO, MediaVideoCreateDTO, MediaVideoUpdateDTO 


class MediaVideoUsecase():
	def __init__(self, repo: MediaVideoRepoInterface):
		self.repo = repo


	def create_video(self, media_video_dto: MediaVideoCreateDTO) -> MediaVideoDTO:
		new_video = MediaVideo(**media_video_dto._asdict())
		stored_video = self.repo.store(new_video)

		return MediaVideoDTO(**stored_video.to_dict())


	def get_video_by_id(self, id: int) -> Optional[MediaVideoDTO]:
		found_video = self.repo.get_by_id(id)

		if found_video is None:
			return None

		return MediaVideoDTO(**found_video.to_dict())


	def get_videos(self, query_parameters_dto: QueryParametersDTO) -> list[MediaVideoDTO]:
		videos = self.repo.get_all(query_parameters_dto)

		return videos


	def get_media_videos(self, media_id: int) -> list[MediaVideoDTO]:
		videos = self.repo.get_media_videos(media_id)

		return videos


	def update_video(self, id: int, update_video_dto: MediaVideoUpdateDTO) -> MediaVideoDTO:
		updated_video = self.repo.update(id, update_video_dto)

		return MediaVideoDTO(**updated_video.to_dict())


	def delete_video(self, id: int) -> MediaVideoDTO:
		deleted_video = self.repo.delete(id=id)

		return MediaVideoDTO(**deleted_video.to_dict())


	def is_field_exists(self, name: str, value: Any) -> bool:
		is_exists = self.repo.is_field_exists({name: value})

		return is_exists
