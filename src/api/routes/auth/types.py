from typing import TypedDict


class Claims(TypedDict):
	type: str = 'access'
	role: str