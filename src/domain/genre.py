from dataclasses import dataclass, asdict

@dataclass
class Genre:
    id: int
    name: str
    slug: str

    # Методы для преобразований в DTO:
    def to_dict(self) -> dict:
        return asdict(self)