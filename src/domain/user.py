from dataclasses import dataclass, asdict
from typing import Optional
import datetime


@dataclass
class User:
	id: str  # Примечание по type hint айдишника (почему не int?): в разных бд это может быть не только int, но и str, как UUID 
	username: str
	password_hash: str
	registration_date: datetime.date
	is_banned: bool = False

	# Примечание по Optional[]: по PEP Optional используется только в случае допущения None, кроме значения объявленного типа
	email: Optional[str] = None
	display_name: Optional[str] = None
	birthday: Optional[datetime.date] = None 
	description: Optional[str] = None
	avatar: Optional[str] = None


	# Методы для преобразований в DTO:
	def to_dict(self) -> dict:
		return asdict(self)
