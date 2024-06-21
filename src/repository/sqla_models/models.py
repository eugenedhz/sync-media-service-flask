from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship

from src.repository.sqla_models.types import DateAsTimestamp
from src.configs.constants import Tables


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
	__tablename__ = Tables.USER

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


class MediaGenreModel(Base):
	__tablename__ = Tables.MEDIA_GENRE

	id = Column(Integer, primary_key=True)

	genreId = Column(Integer, ForeignKey(f'{Tables.GENRE}.id', ondelete='CASCADE'), nullable=False)
	mediaId = Column(Integer, ForeignKey(f'{Tables.MEDIA}.id', ondelete='CASCADE'), nullable=False)


class MediaModel(Base):
	__tablename__ = Tables.MEDIA

	id = Column(Integer, primary_key=True)

	name = Column(String, nullable=False)
	description = Column(String, nullable=False)
	thumbnail = Column(String, nullable=False)
	preview = Column(String, nullable=False)
	trailer = Column(String, nullable=True)

	genres = relationship(
		'GenreModel',
		secondary = MediaGenreModel.__table__,
		back_populates = 'medias'
	)


class GenreModel(Base):
	__tablename__ = Tables.GENRE

	id = Column(Integer, primary_key=True)
	
	slug = Column(String, unique=True, nullable=False)
	name = Column(String, nullable=False)

	medias = relationship(
		'MediaModel',
		secondary = MediaGenreModel.__table__,
		back_populates = 'genres'
	)