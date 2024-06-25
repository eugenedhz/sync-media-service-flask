from typing import TypedDict, NamedTuple


class GenreDTO(NamedTuple):
    id: int
    name: str
    slug: str


class GenreCreateDTO(NamedTuple):
    name: str
    slug: str


class GenreUpdateDTO(TypedDict):
    name: str
    slug: str