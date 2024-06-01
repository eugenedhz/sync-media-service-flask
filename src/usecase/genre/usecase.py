from typing import Optional

from src.domain.genre import Genre
from src.interface.repository.genre import GenreRepoInterface
from src.usecase.dto import QueryParametersDTO
from src.usecase.genre.dto import GenreDTO, GenreCreateDTO


class GenreUseCase():
    def __init__(self, repo: GenreRepoInterface):
        self.repo = repo
    

    def create_genre(self, genre_dto: GenreCreateDTO) -> GenreDTO:
        new_genre = Genre(**genre_dto._asdict())

        stored_genre = self.repo.store(new_genre)

        return GenreDTO(**stored_genre.to_dict())


    def get_by_slug(self, slug: str) -> Optional[GenreDTO]:
        found_genre = self.repo.get_by_slug(slug=slug)
 
        if found_genre is None:
            return None

        return GenreDTO(**found_genre.to_dict())
    

    def get_by_id(self, id: int) -> Optional[GenreDTO]:
        found_genre = self.repo.get_by_id(id=id)

        if found_genre is None:
            return None

        return GenreDTO(**found_genre.to_dict())
    

    def get_genres(self, query_parameters_dto: QueryParametersDTO) -> list[GenreDTO]:
        genres = self.repo.get_all(query_parameters_dto)

        return genres


    def update_genre(self, id: int, update_genre_dto: GenreDTO) -> GenreDTO:
        updated_genre = self.repo.update(id, update_genre_dto)

        return GenreDTO(**updated_genre.to_dict())


    def delete_genre(self, id: int) -> GenreDTO:
        deleted_genre = self.repo.delete(id=id)

        return GenreDTO(**deleted_genre.to_dict())


    def is_field_exists(self, name: str, value: str) -> bool:
        is_exists = self.repo.is_field_exists({name: value})

        return is_exists