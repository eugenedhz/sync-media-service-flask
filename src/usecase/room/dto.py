from typing import NamedTuple, TypedDict, Optional


class RoomDTO(NamedTuple):
	id: int
	name: str
	title: str
	isPrivate: bool
	creatorId: int
	cover: Optional[str]


class RoomCreateDTO(NamedTuple):
	name: str
	title: str
	isPrivate: bool
	creatorId: int
	cover: Optional[str] = None


class RoomUpdateDTO(TypedDict):
	name: str
	title: str
	isPrivate: bool
	cover: str