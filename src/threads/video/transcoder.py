from datetime import datetime

from threading import Thread
from queue import PriorityQueue, Queue

from src.configs.constants import Static
from src.api.services.video import video_service, transcode_session

from pkg.file.filename import get_name


def transcode_video(queue: Queue) -> None:
    while True:
        filename = queue.get()[1]
        upload_session = get_name(filename)

        for quality in Static.VIDEOS_QUALITIES:
            session = upload_session + quality

            # значение сессии = 3 эквивалентно статусу [pending]
            transcode_session.set(session, 3)

        for quality in Static.VIDEOS_QUALITIES:
            session = upload_session + quality

            # значение сессии = 2 эквивалентно статусу [processing]
            transcode_session.set(session, 2)

            output_extension = Static.VIDEOS_TRANSCODED_EXTENSION

            # значения: 1 - ошибка [error], 0 - выполнено [success]
            exit_code = video_service.transcode_video(filename, quality, output_extension)
            current_time = int(datetime.now().timestamp())

            # ставится вместе с временем, чтобы потом очистить
            status = f'{ exit_code } { current_time }'

            transcode_session.set(session, status)

        video_service.delete(filename)
        queue.task_done()


transcode_queue = PriorityQueue()
transcoder = Thread(
    target = transcode_video,
    args = (transcode_queue,),
    daemon = True
)

transcoder.start()
