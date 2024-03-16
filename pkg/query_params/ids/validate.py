def is_valid_ids(ids: tuple[str, ...]) -> bool:
	for id in ids:
		if not id.isdigit():
			return False

	return True