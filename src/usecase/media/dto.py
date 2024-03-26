from typing import TypedDict, NamedTuple, Union, Optional, Any


class MediaDTO(NamedTuple):
    mId: int
    mName: str
    description: str
    thumbnail: str
    preview: str
    ratingId: Optional[int]
    trailer: Optional[int]
    subtitleId: Optional[int]
    genreId: Optional[int]


class MediaCreateDTO(NamedTuple):

    name: str
    description: str
    thumbnail: str
    preview: str


class MediaUpdateDTO(NamedTuple):
    name: str
    description: str
    thumbnail: str
    preview: str
