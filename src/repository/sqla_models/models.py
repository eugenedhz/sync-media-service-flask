from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.ext.associationproxy import association_proxy
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

	requested_rels = relationship(
		'FriendshipRequestModel',
		foreign_keys='FriendshipRequestModel.requesting_user_id',
		backref='requesting_user'
	)
	received_rels = relationship(
		'FriendshipRequestModel',
		foreign_keys='FriendshipRequestModel.receiving_user_id',
		backref='receiving_user'
	)
	aspiring_friends = association_proxy('received_rels', 'requesting_user')
	desired_friends = association_proxy('requested_rels', 'receiving_user')


class MediaModel(Base):
	__tablename__ = Tables.MEDIA

	id = Column(Integer, primary_key=True)

	name = Column(String, nullable=False)
	description = Column(String, nullable=False)
	thumbnail = Column(String, nullable=False)
	preview = Column(String, nullable=False)
	trailer = Column(String, nullable=True)


class FriendshipRequestModel(Base):
	__tablename__ = Tables.FRIENDSHIP_REQUEST

	id = Column(Integer, primary_key=True)

	requesting_user_id = Column(Integer, ForeignKey('User.id', ondelete="CASCADE"), primary_key=True)
	receiving_user_id = Column(Integer, ForeignKey('User.id', ondelete="CASCADE"), primary_key=True)
	is_rejected = Column(Boolean, nullable=False, default=False)


class FriendshipModel(Base):
	__tablename__ = Tables.FRIENDSHIP

	id = Column(Integer, primary_key=True)

	user_1 = Column(Integer, ForeignKey('User.id', ondelete="CASCADE"), primary_key=True)
	user_2 = Column(Integer, ForeignKey('User.id', ondelete="CASCADE"), primary_key=True)
