from typing import Optional


def convert_string(value: str) -> Optional[int | str | bool]:
	conversions = {
		'null': None,
		'false': False,
		'true': True
	}

	if value.isdigit():
		value = int(value)
	if value in conversions:
		value = conversions[value]

	return value