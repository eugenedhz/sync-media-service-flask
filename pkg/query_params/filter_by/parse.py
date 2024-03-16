from typing import Optional


def parse_filter_by(filter_by: Optional[str], valid_fields: tuple[str, ...]) -> Optional[dict]:
	if filter_by is None:
		return None

	parsed_filter_by = dict()
	splitted_filter_by = filter_by.split(',')

	for field in splitted_filter_by:
		splitted_field = field.split('=')
		if len(splitted_field) != 2:
			continue

		key = splitted_field[0]
		value = splitted_field[1]

		if key in valid_fields:
			parsed_filter_by[key] = value

	if len(parsed_filter_by) == 0:
		return None

	return parsed_filter_by