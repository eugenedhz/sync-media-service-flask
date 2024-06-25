from dataclasses import dataclass
from typing import Optional
import datetime

from src.domain.base import Base


@dataclass
class User(Base):
	username: str
	passwordHash: str
	registrationDate: int # timestamp
	email: str
	displayName: str
	isBanned: bool = False

	id: Optional[int] = None
	birthday: Optional[int] = None # timestamp
	description: Optional[str] = None
	avatar: Optional[str] = None
