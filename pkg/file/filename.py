from typing import NamedTuple
from os.path import basename, splitext


class Filename(NamedTuple):
    name: str
    extension: str

    def filename(self):
        return self.name + self.extension


def split_filename(filename: str) -> Filename:
	filename = basename(filename)

	return Filename(*splitext(filename))