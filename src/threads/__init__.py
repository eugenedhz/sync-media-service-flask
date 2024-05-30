from src.threads.video.cleaner import cleaner
from src.threads.video.transcoder import transcoder


cleaner.start()
transcoder.start()