from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class UserModel(Base):
	__tablename__ = 'User'

	id = Column(Integer, primary_key=True)

	username = Column(String, unique=True, nullable=False)
	passwordHash = Column(String, nullable=False)
	registrationDate = Column(DateTime, nullable=False)
	isBanned = Column(Boolean, nullable=False, default=False)

	email = Column(String, unique=True)
	displayName = Column(String)
	birthday = Column(DateTime)
	description = Column(String)
	avatar = Column(String)