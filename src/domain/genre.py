from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Genre:
    name: str
    slug: str

    id: Optional[int] = None

    # Методы для преобразований в DTO:
    def to_dict(self) -> dict:
        return asdict(self)