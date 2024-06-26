from typing import NamedTuple, TypedDict, Optional


class MediaVideoDTO(NamedTuple):
	id: int
	mediaId: int
	name: str
	source: str
	language: str


class MediaVideoCreateDTO(NamedTuple):
	mediaId: int
	name: str
	source: str
	language: str


class MediaVideoUpdateDTO(TypedDict):
	name: str
	source: str
	language: str
