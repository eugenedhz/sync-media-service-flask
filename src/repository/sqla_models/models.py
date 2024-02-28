from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class User(Base):
	id = Column(Integer, primary_key=True)

	username = Column(String, unique=True, nullable=False)
	password_hash = Column(String, nullable=False)
	registration_date = Column(DateTime, nullable=False)
	is_banned = Column(Boolean, nullable=False, default=False)

	email = Column(String, unique=True)
	display_name = Column(String)
	birthday = Column(DateTime)
	description = Column(String)
	avatar = Column(String)