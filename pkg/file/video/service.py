from pkg.file.file_service import FileService
from pkg.ffmpeg.video import transcode
from pkg.file.filename import split_filename


class VideoService(FileService):
	def write_chunk(self, data: bytes, chunk_offset: int, filename: str) -> None:
		path = self.destination_path + filename

		with open(path, 'ab') as file:
			file.seek(chunk_offset)
			file.write(data)


	def transcode(self, filename: str, quality: str, output_extension: str) -> int:
		input_path = self.destination_path + filename
		name = split_filename(filename).name
		output_path = self.destination_path + name + quality + output_extension

		exit_code = transcode(input_path, output_path, quality)

		return exit_code
