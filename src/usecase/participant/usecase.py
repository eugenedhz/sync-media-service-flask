from typing import Any, Optional

from src.domain.participant import Participant
from src.interface.repository.participant import ParticipantRepoInterface
from src.usecase.dto import QueryParametersDTO
from src.usecase.participant.dto import ParticipantDTO, ParticipantCreateDTO


class ParticipantUsecase():
	def __init__(self, repo: ParticipantRepoInterface):
		self.repo = repo


	def create_participant(self, participant_dto: ParticipantCreateDTO) -> ParticipantDTO:
		new_participant = Participant(**participant_dto._asdict())

		return self.repo.store(new_participant)


	def get_participant_by_id(self, id: int) -> Optional[ParticipantDTO]:
		found_participant = self.repo.get_by_id(id)

		if found_participant is None:
			return None

		return found_participant


	def get_participants(self, query_parameters_dto: QueryParametersDTO) -> list[ParticipantDTO]:
		participants = self.repo.get_all(query_parameters_dto)

		return participants


	def get_room_participants(self, room_id: int) -> list[ParticipantDTO]:
		participants = self.repo.get_room_participants(room_id)

		return participants


	def delete_participant(self, id: int) -> ParticipantDTO:
		deleted_participant = self.repo.delete(id)

		return deleted_participant


	def is_field_exists(self, name: str, value: Any) -> bool:
		is_exists = self.repo.is_field_exists({name: value})

		return is_exists
