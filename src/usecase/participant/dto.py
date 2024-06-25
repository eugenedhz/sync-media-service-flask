from typing import NamedTuple, Optional


class ParticipantDTO(NamedTuple):
	id: int
	roomId: int
	userId: int
	name: str
	avatar: Optional[str]


class ParticipantCreateDTO(NamedTuple):
	roomId: int
	userId: int
