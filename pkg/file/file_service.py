from typing import Optional

import os
from glob import glob
from uuid import uuid4

from pkg.file.filename import split_filename


class FileService():
	def __init__(self, destination_path: str):
		if not destination_path.endswith('/'):
			destination_path += '/'

		self.destination_path = destination_path


	# Пометка: генерирует уникальное имя файла, возвращает его
	def save(self, data: bytes, extension: str) -> str:
		if not extension.startswith('.'):
			extension = '.' + extension

		filename = uuid4().hex + extension
		path = self.destination_path + filename

		with open(path, 'wb') as file:
			file.write(data)

		return filename


	def find_file(self, name: str) -> Optional[str]:
		pattern = f'{ self.destination_path }{ name }*'

		filenames = glob(pattern)
		if len(filenames) == 0:
			return None

		return split_filename(filenames[0]).filename()


	def file_size(self, filename: str) -> int:
		path = self.destination_path + filename

		return os.path.getsize(path)


	def delete(self, filename: str) -> None:
		path = self.destination_path + filename
		os.remove(path)