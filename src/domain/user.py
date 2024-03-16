from dataclasses import dataclass, asdict
from typing import Optional
import datetime


@dataclass
class User:
	username: str
	passwordHash: str
	registrationDate: int # timestamp
	email: str
	displayName: str
	isBanned: bool = False

	# Примечание по Optional[]: по PEP Optional используется только в случае допущения None, кроме значения объявленного типа
	id: Optional[str] = None # Примечание по type hint айдишника (почему не int?): в разных бд это может быть не только int, но и str, как UUID 
	birthday: Optional[int] = None # timestamp
	description: Optional[str] = None
	avatar: Optional[str] = None


	# Методы для преобразований в DTO:
	def to_dict(self) -> dict:
		return asdict(self)
