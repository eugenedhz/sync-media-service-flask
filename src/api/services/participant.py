from src.usecase.participant.usecase import ParticipantUsecase
from src.repository.participant.repo import ParticipantRepo
from src.repository.driver.postgres import postgresql_engine


repo = ParticipantRepo(postgresql_engine)
participant_service = ParticipantUsecase(repo)