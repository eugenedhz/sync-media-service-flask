from os.path import basename, splitext


def get_filename(path: str) -> str:
	return basename(path)


def get_extension(filename: str) -> str:
	return splitext(filename)[1]


def get_name(filename: str) -> str:
	filename = get_filename(filename)

	return filename.split('.')[0]