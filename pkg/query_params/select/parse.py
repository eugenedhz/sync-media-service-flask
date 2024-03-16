from typing import Optional


def parse_select(select_fields: Optional[str], valid_fields: tuple[str, ...]) -> Optional[tuple[str, ...]]:
	if select_fields is None:
		return None

	splitted_select_fields = select_fields.split(',')
	
	select_fields_set = set(splitted_select_fields)
	valid_fields_set = set(valid_fields)

	filtered_select_fields = select_fields_set.intersection(valid_fields_set)

	return (tuple(filtered_select_fields) if len(filtered_select_fields) != 0 else None)