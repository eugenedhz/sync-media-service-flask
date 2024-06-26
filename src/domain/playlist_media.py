from dataclasses import dataclass
from typing import Optional

from src.domain.base import Base


@dataclass
class PlaylistMedia(Base):
    roomId: int
    mediaId: int
    
    id: Optional[int] = None
    order: Optional[int] = None