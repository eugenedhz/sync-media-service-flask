from abc import ABC, abstractmethod
from typing import Any

from src.usecase.dto import QueryParametersDTO
from src.usecase.genre.dto import GenreDTO, GenreUpdateDTO
from src.domain.genre import Genre


class GenreRepoInterface(ABC):
	@abstractmethod
	def store(self, genre: Genre) -> Genre:
		raise NotImplementedError


	@abstractmethod
	def get_by_id(self, id: int) -> Genre:
		raise NotImplementedError


	@abstractmethod
	def get_by_slug(self, slug: str) -> Genre:
		raise NotImplementedError


	@abstractmethod
	def update(self, id: int, update_genre_dto: GenreUpdateDTO) -> Genre:
		raise NotImplementedError


	@abstractmethod
	def get_all(self, query_parameters_dto: QueryParametersDTO) -> list[GenreDTO]:
		raise NotImplementedError


	@abstractmethod
	def get_media_genres(self, media_id: int) -> list[GenreDTO]:
		raise NotImplementedError


	@abstractmethod
	def is_media_genre_exist(self, media_id: int, genre_id: int) -> bool:
		raise NotImplementedError


	@abstractmethod
	def add_genre_to_media(self, media_id: int, genre_id: int) -> Genre:
		raise NotImplementedError


	@abstractmethod
	def delete_genre_from_media(self, media_id: int, genre_id: int) -> Genre:
		raise NotImplementedError


	@abstractmethod
	def get_media_genres(self, media_id: int) -> list[GenreDTO]:
		raise NotImplementedError


	@abstractmethod
	def delete(self, id: int) -> Genre:
		raise NotImplementedError


	@abstractmethod
	def is_field_exists(self, field: dict[str: Any]) -> bool:
		raise NotImplementedError
