from sqlalchemy import Engine, update, select
from sqlalchemy.orm import Session
from typing import Any
 
from src.domain.genre import Genre
from src.interface.repository.genre import GenreRepoInterface
from src.repository.sqla_models.models import GenreModel
from src.usecase.dto import QueryParametersDTO
from src.usecase.genre.dto import GenreDTO

from pkg.sqlalchemy.utils import get_first, get_all, formalize_filters


class GenreRepo(GenreRepoInterface):
    def __init__(self, engine: Engine):
        self.engine = engine


    def store(self, genre: Genre) -> Genre:
        with Session(self.engine) as s:
            new_genre = GenreModel(**(genre.to_dict()))

            s.add(new_genre)

            s.commit()

            s.refresh(new_genre)

        return Genre(**new_genre._asdict(Genre))


    def get_by_id(self, id: int) -> Genre:
        with Session(self.engine) as s:
            query = (
                select(GenreModel)
                .where(GenreModel.id == id)
            )

            found_genre = get_first(session=s, query=query)

        if found_genre is None:
            return None

        return Genre(**found_genre._asdict(Genre))


    def get_by_slug(self, slug: str) -> Genre:
        with Session(self.engine) as s:
            query = (
				select(GenreModel)
				.where(GenreModel.slug == slug)
			)

            found_genre = get_first(session=s, query=query)

        if found_genre is None:
            return None

        return Genre(**found_genre._asdict(Genre))
    

    def update(self, id: int, update_genre_dto: GenreDTO) -> Genre:
        with Session(self.engine) as s:
            query = (
                update(GenreModel)
                .where(GenreModel.id == id)
                .values(**update_genre_dto)
            )

            s.execute(query)

            s.commit()

            updated_genre = s.get(GenreModel, id)

        return Genre(**updated_genre._asdict(Genre))


    def get_all(self, query_parameters: QueryParametersDTO) -> list[GenreDTO]:
        with Session(self.engine) as s:
            query = (
                select(GenreModel)
            )

            filters = query_parameters.filters

            if filters is not None:
                filters = formalize_filters(filters, GenreModel)
                query = query.filter(*filters)

            found_genres = get_all(session=s, query=query)

        found_genres_dto = [GenreDTO(**genre._asdict(Genre)) for genre in found_genres]

        return found_genres_dto


    def delete(self, id: int) -> Genre:
        with Session(self.engine) as s:
            found_genre = s.get(GenreModel, id)

            s.delete(found_genre)

            s.commit()

        return Genre(**found_genre._asdict(Genre))


    def is_field_exists(self, field: dict[str: Any]) -> bool:
        with Session(self.engine) as s:
            query = (
                select(GenreModel.id)
                .filter_by(**field)
            )

            found_genre = get_first(session=s, query=query)

        return found_genre is not None