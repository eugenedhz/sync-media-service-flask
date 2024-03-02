from dataclasses import dataclass, asdict
from typing import Optional
import datetime


@dataclass
class User:
	username: str
	passwordHash: str
	registrationDate: datetime.date
	isBanned: bool = False

	# Примечание по Optional[]: по PEP Optional используется только в случае допущения None, кроме значения объявленного типа
	id: Optional[str] = None # Примечание по type hint айдишника (почему не int?): в разных бд это может быть не только int, но и str, как UUID 
	email: Optional[str] = None
	displayName: Optional[str] = None
	birthday: Optional[datetime.date] = None 
	description: Optional[str] = None
	avatar: Optional[str] = None


	# Методы для преобразований в DTO:
	def to_dict(self) -> dict:
		return asdict(self)
