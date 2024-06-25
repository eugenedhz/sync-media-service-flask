from copy import deepcopy

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from src.repository.sqla_models.types import DateAsTimestamp
from src.configs.constants import Tables


class Base(DeclarativeBase):
	def _asdict(self, domain_class):
		new_dict = deepcopy(self.__dict__)
		required_fields = domain_class.__match_args__
		fields_to_check = tuple(new_dict.keys())

		for key in fields_to_check:
			if key not in required_fields:
				del new_dict[key]

		return new_dict


class ParticipantModel(Base):
	__tablename__ = Tables.PARTICIPANT

	id = Column(Integer, primary_key=True)
	roomId = Column(Integer, ForeignKey(f'{Tables.ROOM}.id', ondelete='CASCADE'), nullable=False)
	userId = Column(Integer, ForeignKey(f'{Tables.USER}.id', ondelete='CASCADE'), nullable=False)

	user = relationship('UserModel', back_populates='participations')
	room = relationship('RoomModel', back_populates='participants')


	@hybrid_property
	def name(self) -> str:
		return self.user.displayName


	@hybrid_property
	def avatar(self) -> str:
		return self.user.avatar


class RoomModel(Base):
	__tablename__ = Tables.ROOM

	id = Column(Integer, primary_key=True)
	creatorId = Column(Integer, ForeignKey(f'{Tables.USER}.id'), nullable=False)

	name = Column(String, nullable=False, unique=True)
	title = Column(String, nullable=False)
	isPrivate = Column(Boolean, nullable=False)
	cover = Column(String)

	participants = relationship(
		ParticipantModel,
		back_populates = 'room'
	)


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

	createdRooms = relationship(
		RoomModel, 
		cascade = 'all, delete-orphan',
		backref = 'creator'
	)
	participations = relationship(
		ParticipantModel,
		back_populates = 'user'
	)


class MediaGenreModel(Base):
	__tablename__ = Tables.MEDIA_GENRE

	id = Column(Integer, primary_key=True)

	genreId = Column(Integer, ForeignKey(f'{Tables.GENRE}.id', ondelete='CASCADE'), nullable=False)
	mediaId = Column(Integer, ForeignKey(f'{Tables.MEDIA}.id', ondelete='CASCADE'), nullable=False)


class VideoModel(Base):
	__tablename__ = Tables.MEDIA_VIDEO

	id = Column(Integer, primary_key=True)
	mediaId = Column(Integer, ForeignKey(f'{Tables.MEDIA}.id'), nullable=False)
	name = Column(String, nullable=False)
	source = Column(String, unique=True, nullable=False)
	language = Column(String, nullable=False)


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
	videos = relationship(
		VideoModel,
		cascade = 'all, delete-orphan',
		backref = 'media'
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


class FriendshipRequestModel(Base):
	__tablename__ = Tables.FRIENDSHIP_REQUEST

	id = Column(Integer, primary_key=True, autoincrement=True)

	requesting_user_id = Column(Integer, ForeignKey(f'{Tables.USER}.id', ondelete="CASCADE"), nullable=False)
	receiving_user_id = Column(Integer, ForeignKey(f'{Tables.USER}.id', ondelete="CASCADE"), nullable=False)


class FriendshipModel(Base):
	__tablename__ = Tables.FRIENDSHIP

	id = Column(Integer, primary_key=True, autoincrement=True)

	user_1 = Column(Integer, ForeignKey(f'{Tables.USER}.id', ondelete="CASCADE"), nullable=False)
	user_2 = Column(Integer, ForeignKey(f'{Tables.USER}.id', ondelete="CASCADE"), nullable=False)
>>>>>>> src/repository/sqla_models/models.py
