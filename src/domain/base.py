from dataclasses import asdict


class Base:
	def to_dict(self) -> dict:
		return asdict(self)