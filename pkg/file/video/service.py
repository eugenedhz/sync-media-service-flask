from pkg.file.file_service import FileService
from pkg.ffmpeg.video import transcode


class VideoService(FileService):
	def write_chunk(self, data: bytes, chunk_offset: int, filename: str) -> None:
		path = self.destination_path + filename

		with open(path, 'ab') as file:
			file.seek(chunk_offset)
			file.write(data)


	def transcode_video(self, filename: str, size: str) -> int:
		input = self.destination_path + filename
		name, _ = filename.split('.')
		output = self.destination_path + name + size + '.mp4'

		exit_code = transcode(input, output, size)

		return exit_code
