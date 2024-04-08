from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase
from src.repository.sqla_models.types import DateAsTimestamp


class Base(DeclarativeBase):
	def _asdict(self, domain_class):
		new_dict = self.__dict__
		required_fields = domain_class.__match_args__
		fields_to_check = tuple(new_dict.keys())

		for key in fields_to_check:
			if key not in required_fields:
				del new_dict[key]

		return new_dict


class UserModel(Base):
	__tablename__ = 'User'

	id = Column(Integer, primary_key=True)

	username = Column(String, unique=True, nullable=False)
	passwordHash = Column(String, nullable=False)
	registrationDate = Column(DateAsTimestamp, nullable=False)
	isBanned = Column(Boolean, nullable=False, default=False)
	email = Column(String, unique=True, nullable=False)
	displayName = Column(String, nullable=False)

	birthday = Column(DateAsTimestamp)
	description = Column(String)
	avatar = Column(String)


class MediaModel(Base):
	__tablename__ = 'Media'

	id = Column(Integer, primary_key=True)

	name = Column(String, nullable=False)
	description = Column(String, nullable=True)
	thumbnail = Column(String, nullable=False)
	preview = Column(String, nullable=False)
	trailer = Column(String, nullable=True)
