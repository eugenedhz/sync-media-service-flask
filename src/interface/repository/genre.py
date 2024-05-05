from abc import ABC, abstractmethod
from typing import Any

from src.usecase.dto import QueryParametersDTO
from src.usecase.genre.dto import GenreUpdateDTO, GenreDTO
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
	def delete(self, id: int) -> Genre:
		raise NotImplementedError


	@abstractmethod
	def is_field_exists(self, field: dict[str: Any]) -> bool:
		raise NotImplementedError
