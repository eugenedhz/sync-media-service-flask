from typing import Optional


def parse_filter_by(filter_query: Optional[str], valid_fields: dict[str, type]) -> Optional[dict]:
	if filter_query is None:
		return None

	valid_filters = dict()
	filters = filter_query.split(',')
	conversions = {
		'null': None,
		'false': False,
		'true': True
	}

	for filter in filters:
		if len(filter.split('=')) != 2:
			raise KeyError

		key, value = filter.split('=')

		if value.isdigit():
			value = int(value)
		if value in conversions:
			value = conversions[value]

		if key in valid_fields:
			if not isinstance(value, valid_fields[key]):
				raise TypeError
			valid_filters[key] = value
		else:
			raise KeyError

	return valid_filters