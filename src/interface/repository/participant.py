from abc import ABC, abstractmethod

from typing import Any

from src.domain.participant import Participant
from src.usecase.dto import QueryParametersDTO
from src.usecase.participant.dto import ParticipantDTO


class ParticipantRepoInterface(ABC):
	@abstractmethod
	def store(self, participant: Participant) -> ParticipantDTO:
		raise NotImplementedError


	@abstractmethod
	def get_by_id(self, id: int) -> ParticipantDTO:
		raise NotImplementedError


	@abstractmethod
	def delete(self, id: int) -> ParticipantDTO:
		raise NotImplementedError


	@abstractmethod
	def get_all(self, query_parameters: QueryParametersDTO) -> list[ParticipantDTO]:
		raise NotImplementedError


	@abstractmethod
	def get_room_participants(self, room_id: int) -> list[ParticipantDTO]:
		raise NotImplementedError


	@abstractmethod
	def is_field_exists(self, field: dict[str: Any]) -> bool:
		raise NotImplementedError
