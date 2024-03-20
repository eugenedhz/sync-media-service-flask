from src.configs.constants import Static
from pkg.file.file_service import FileService


image_service = FileService(destination_path=Static.IMAGES_FOLDER)