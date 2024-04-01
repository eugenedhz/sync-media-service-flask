from typing import TypedDict, NamedTuple, Union, Optional, Any


class MediaDTO(NamedTuple):
    id: int
    name: str
    description: str
    thumbnail: str
    preview: str
    trailer: Optional[str]


class MediaCreateDTO(NamedTuple):

    name: str
    description: str
    thumbnail: str
    preview: str


class MediaUpdateDTO(TypedDict):
    id: int
    name: str
    description: str
    thumbnail: str
    preview: str
