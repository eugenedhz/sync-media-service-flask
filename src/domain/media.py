from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Media:
    name: str
    thumbnail: str
    preview: str
    trailer: Optional[str] = None
    id: Optional[int] = None
    description: Optional[str] = None

    # Методы для преобразований в DTO:
    def to_dict(self) -> dict:
        return asdict(self)
