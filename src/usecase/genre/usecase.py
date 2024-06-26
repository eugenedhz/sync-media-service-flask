from typing import Optional

from src.domain.genre import Genre
from src.interface.repository.genre import GenreRepoInterface
from src.usecase.dto import QueryParametersDTO
from src.usecase.genre.dto import GenreDTO, GenreCreateDTO, GenreUpdateDTO


class GenreUsecase():
    def __init__(self, repo: GenreRepoInterface):
        self.repo = repo
    

    def create_genre(self, genre_dto: GenreCreateDTO) -> GenreDTO:
        new_genre = Genre(**genre_dto._asdict())

        stored_genre = self.repo.store(new_genre)

        return GenreDTO(**stored_genre.to_dict())


    def get_genre_by_slug(self, slug: str) -> Optional[GenreDTO]:
        found_genre = self.repo.get_by_slug(slug=slug)
 
        if found_genre is None:
            return None

        return GenreDTO(**found_genre.to_dict())
    

    def get_genre_by_id(self, id: int) -> Optional[GenreDTO]:
        found_genre = self.repo.get_by_id(id=id)

        if found_genre is None:
            return None

        return GenreDTO(**found_genre.to_dict())
    

    def get_genres(self, query_parameters_dto: QueryParametersDTO) -> list[GenreDTO]:
        genres = self.repo.get_all(query_parameters_dto)

        return genres


    def get_media_genres(self, media_id: int) -> list[GenreDTO]:
        genres = self.repo.get_media_genres(media_id)

        return genres


    def is_media_genre_exist(self, media_id: int, genre_id: int) -> bool:
        return self.repo.is_media_genre_exist(media_id=media_id, genre_id=genre_id)


    def add_genre_to_media(self, media_id: int, genre_id: int) -> GenreDTO:
        genre = self.repo.add_genre_to_media(media_id=media_id, genre_id=genre_id)

        return GenreDTO(**genre.to_dict())


    def delete_genre_from_media(self, media_id: int, genre_id: int) -> GenreDTO:
        genre = self.repo.delete_genre_from_media(media_id=media_id, genre_id=genre_id)

        return GenreDTO(**genre.to_dict())


    def update_genre(self, id: int, update_genre_dto: GenreUpdateDTO) -> GenreDTO:
        updated_genre = self.repo.update(id, update_genre_dto)

        return GenreDTO(**updated_genre.to_dict())


    def delete_genre(self, id: int) -> GenreDTO:
        deleted_genre = self.repo.delete(id=id)

        return GenreDTO(**deleted_genre.to_dict())


    def is_field_exists(self, name: str, value: str) -> bool:
        is_exists = self.repo.is_field_exists({name: value})

        return is_exists