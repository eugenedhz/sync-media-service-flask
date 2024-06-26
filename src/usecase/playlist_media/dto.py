from typing import NamedTuple, TypedDict, Optional


class PlaylistMediaDTO(NamedTuple):
	id: int
	roomId: int
	mediaId: int
	order: int
	name: str
	thumbnail: str


class PlaylistMediaCreateDTO(NamedTuple):
	roomId: int
	mediaId: int


class PlaylistMediaUpdateDTO(TypedDict):
	order: int