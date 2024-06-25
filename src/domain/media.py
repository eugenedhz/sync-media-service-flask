from dataclasses import dataclass
from typing import Optional

from src.domain.base import Base


@dataclass
class Media(Base):
    name: str
    thumbnail: str
    preview: str
    description: str
    
    trailer: Optional[str] = None
    id: Optional[int] = None
