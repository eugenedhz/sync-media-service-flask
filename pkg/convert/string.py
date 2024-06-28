from typing import Optional


CONVERSIONS = {
	'null': None,
	'false': False,
	'true': True
}


def convert_string(value: str, t: type) -> Optional[int | str | bool]:
	if isinstance(t, str):
		return value
	if isinstance(t, Optional[str]):
		if value == 'null':
			return None
		return value
	if value.isdigit():
		try:
			return int(value)
		except:
			return float(value)
	if value in conversions:
		return conversions[value]

	return value
