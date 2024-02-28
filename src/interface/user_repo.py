from abc import ABC, abstractmethod


class UserRepoInterface(ABC):
	@abstractmethod
	def get_by_id(self, id: int):
		raise NotImplemented