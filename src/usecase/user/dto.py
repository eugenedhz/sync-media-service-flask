from typing import TypedDict, NamedTuple, Union, Optional, Any


class UserCreateDTO(NamedTuple):
	username: str
	displayName: str
	email: str
	password: str


class UserCheckPasswordDTO(NamedTuple):
	username: str
	password: str


class UserDTO(NamedTuple):
	id: int
	username: str
	displayName: str
	email: str
	registrationDate: int # timestamp
	isBanned: bool
	birthday: Optional[int] # timestamp
	description: Optional[str]
	avatar: Optional[str]


class UserUpdateDTO(TypedDict):
	username: str
	displayName: str
	email: str
	birthday: int # timestamp
	description: str
	avatar: str
