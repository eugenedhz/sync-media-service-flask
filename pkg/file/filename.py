from typing import NamedTuple
from os.path import basename, splitext


class SplittedFilename(NamedTuple):
    name: str
    extension: str

    def filename(self):
        return self.name + self.extension


def split_filename(filename: str) -> SplittedFilename:
	filename = basename(filename)

	return Filename(*splitext(filename))