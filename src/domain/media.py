from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Media:
    mName: str
    description: str
    thumbnail: str
    preview: str
    # Примечание по Optional[]: по PEP Optional используется только в случае допущения None, кроме значения объявленного типа
    ratingId: Optional[int] = None
    trailer: Optional[int] = None
    genreId: Optional[int] = None
    subtitleId: Optional[int] = None
    mId: Optional[int] = None

    # Методы для преобразований в DTO:
    def to_dict(self) -> dict:
        return asdict(self)
