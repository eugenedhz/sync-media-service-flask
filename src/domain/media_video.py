from dataclasses import dataclass
from typing import Optional

from src.domain.base import Base


@dataclass
class MediaVideo(Base):
    mediaId: int
    name: str
    source: str
    language: str
    
    id: Optional[int] = None
