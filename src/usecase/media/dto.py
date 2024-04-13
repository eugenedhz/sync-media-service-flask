from typing import TypedDict, NamedTuple, Optional


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
    trailer: Optional[str] = None


class MediaUpdateDTO(TypedDict):
    name: str
    description: str
    thumbnail: str
    preview: str
    trailer: str
