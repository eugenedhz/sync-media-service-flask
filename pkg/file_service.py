import os
from uuid import uuid4
from typing import Optional


class FileService():
	def __init__(self, destination_path: str):
		if not destination_path.endswith('/'):
			destination_path += '/'

		self.destination_path = destination_path
		self.saved_filename = None


	# Пометка: генерирует уникальное имя файла, сохраняет его в self.saved_filename
	def save(self, data: bytes, extension: str) -> None:
		if not extension.startswith('.'):
			extension = '.' + extension

		filename = uuid4().hex + extension
		path = self.destination_path + filename

		with open(path, 'wb') as file:
			file.write(data)

		self.saved_filename = filename


	def delete(self, filename: str) -> None:
		path = self.destination_path + filename
		os.remove(path)