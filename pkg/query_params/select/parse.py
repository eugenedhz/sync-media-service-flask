from typing import Optional


def parse_select(select: Optional[str], valid_fields: tuple[str, ...], splitter: str) -> Optional[tuple[str, ...]]:
	if select is None:
		return None

	select = select.split(splitter)

	for field in select:
		if field not in valid_fields:
			raise KeyError

	return select