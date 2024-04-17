from threading import Thread
from queue import PriorityQueue, Queue

from src.configs.constants import Static
from src.api.services.video import video_service, transcode_session


def transcode_video(queue: Queue) -> None:
    while True:
        filename = queue.get()
        upload_session = filename[1].split('.')[0]

        for size in Static.VIDEO_SIZES:
            session = upload_session + size

            # значение сессии = 3 эквивалентно статусу [pending]
            transcode_session.set(session, 3)

        for size in Static.VIDEO_SIZES:
            session = upload_session + size

            # значение сессии = 2 эквивалентно статусу [processing]
            transcode_session.set(session, 2)

            # значения сессии = 1 - статус ошибка [error], 0 - статус выполнено [success]
            status = video_service.transcode_video(filename[1], size)
            transcode_session.set(session, status)

        queue.task_done()


transcode_queue = PriorityQueue()
transcoder = Thread(
    target = transcode_video,
    args = (transcode_queue,),
    daemon = True
)

transcoder.start()
