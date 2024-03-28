from typing import Optional, Any, NamedTuple
import re

from pkg.convert.string import convert_string


class Filter(NamedTuple):
	field: str
	operator: str
	value: Any


def parse_filter_by(filter_query: Optional[str], valid_fields: dict[str, type]) -> Optional[list[Filter]]:
	if filter_query is None:
		return None

	valid_filters = []
	filters = filter_query.split(',')

	# регулярка для отдельных фильтров, например, id{>}14 или name{in}[name;name2]...
	filter_pattern = r'^\S+({(==|!=|<|>|<=|>=|)}\S+|{(in|!in)}\[.+\])$'
	operators = ('{<=}', '{>=}', '{==}', '{!=}', '{<}', '{>}', '{in}', '{!in}')
	bool_operators = ('==', '!=')
	list_operators = ('in', '!in')

	for filter in filters:
		if re.match(filter_pattern, filter) is None:
			raise TypeError

		for operator in operators:
			if operator in filter:
				field, value = filter.split(operator)
				found_operator = operator.strip('{}')
				break

		if field not in valid_fields:
			raise KeyError

		if found_operator in list_operators:
			value = value.strip('[]').split(';')
			for i in range(len(value)):
				value[i] = convert_string(value[i])
		else:
			value = convert_string(value)

		if isinstance(value, Optional[bool]):
			if found_operator not in bool_operators:
				raise TypeError

		if isinstance(value, list):
			for val in value:
				if not isinstance(val, valid_fields[field]):
					raise TypeError
		else:
			if not isinstance(value, valid_fields[field]):
				raise TypeError
		
		valid_filters.append(Filter(field, found_operator, value))
			

	return valid_filters