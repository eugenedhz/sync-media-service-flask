from typing import TypedDict, NamedTuple, Union, Optional


class UserRegisterDTO(NamedTuple):
	username: str
	displayName: str
	email: str
	password: str


class LoginDTO(NamedTuple):
	username: str
	password: str


class UserDTO(NamedTuple):
	id: Union[str | int]
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