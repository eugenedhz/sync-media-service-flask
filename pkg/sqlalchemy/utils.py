from sqlalchemy.orm import Session
from sqlalchemy import Select
from sqlalchemy.engine import Row


def get_first(session: Session, query: Select) -> Row:
	return session.scalars(query).first()


def get_all(session: Session, query: Select) -> list[Row]:
	return session.scalars(query).all()