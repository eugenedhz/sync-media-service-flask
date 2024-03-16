from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.types import TypeDecorator
from datetime import datetime


class Base(DeclarativeBase):
	def _asdict(self, domain_class):
		new_dict = self.__dict__
		required_fields = domain_class.__match_args__
		fields_to_check = tuple(new_dict.keys())

		for key in fields_to_check:
			if key not in required_fields:
				del new_dict[key]

		return new_dict


class DateAsTimestamp(TypeDecorator):
    cache_ok = True
    impl = DateTime

    def process_bind_param(self, value, dialect):
        if value is not None:
            return datetime.fromtimestamp(value)

    def process_result_value(self, value, dialect):
        if value is not None:
            return int(value.timestamp())


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