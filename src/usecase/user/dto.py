from typing import NamedTuple


class UserRegisterDTO(NamedTuple):
	username: str
	displayName: str
	email: str
	passwordHash: str
