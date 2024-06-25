from dataclasses import dataclass
from typing import Optional
import datetime

from src.domain.base import Base


@dataclass
class Room(Base):
	name: str
	title: str
	isPrivate: bool
	creatorId: int

	id: Optional[int] = None
	cover: Optional[str] = None
