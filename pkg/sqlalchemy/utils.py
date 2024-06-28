from operator import lt, le, eq, ne, ge, gt

from sqlalchemy.orm import Session
from sqlalchemy import Select, or_, and_
from sqlalchemy.engine import ScalarResult
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql.elements import BinaryExpression

from pkg.query_params.filter_by.parse import Filter


def get_first(session: Session, query: Select) -> ScalarResult:
	return session.scalars(query).first()


def get_all(session: Session, query: Select) -> list[ScalarResult]:
	return session.scalars(query).all()


def formalize_filters(filters: list[Filter], Model: DeclarativeBase) -> list[BinaryExpression]:
	formalized_filters = []
	operators = {
		'==': eq,
		'!=': ne,
		'>': gt,
		'<': lt,
		'>=': ge,
		'<=': le
	}

	for filter in filters:
		column = filter.field
		operator = filter.operator
		value = filter.value
		attribute = getattr(Model, column)

		if operator == 'in':
			# проверка на None, потому что sqlalchemy не может сравнивать None в .in_ (также в .not_in)
			if None in value:
				filter = or_(attribute.in_(value), attribute.is_(None))
			else:
				filter = attribute.in_(value)

		elif operator == '!in':
			if None in value:
				# очистка списка от None, потому что .not_in в sqlalchemy почему-то с value=[None] ничего не найдёт (криворуки)
				value = [val for val in value if val != None]
				filter = and_(attribute.not_in(value), attribute.is_not(None))
			else:
				filter = or_(attribute.not_in(value), attribute.is_(None))

		elif operator == '~':
			if len(value) == 0:
				# стопроцентно ничего не найдёт, т.к. не должно быть пустых строк
				filter = operators['=='](attribute, '')
			else:
				filter = or_(*[attribute.ilike(f'%{word}%') for word in value])

		else:
			filter = operators[operator](attribute, value)
		
		formalized_filters.append(filter)

	return formalized_filters