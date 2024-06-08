from dataclasses import dataclass
from typing import Optional

from src.domain.base import Base


@dataclass
class Participant(Base):
    roomId: int
    userId: int
    
    id: Optional[int] = None
