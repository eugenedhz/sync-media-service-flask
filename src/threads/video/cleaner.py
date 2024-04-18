from datetime import datetime
from threading import Thread
from time import sleep

from src.configs.constants import Session
from src.api.services.video import video_service, upload_session, transcode_session


def remove_inactive_sessions() -> None:
    while True:
        current_time = datetime.now()

        for session in upload_session.keys():
            timestamp = upload_session.get(session)
            last_access = datetime.fromtimestamp(timestamp)

            if current_time - last_access > Session.UPLOAD_TIMEOUT:
                upload_session.delete(session)
                filename = video_service.find_file(session)

                if filename != None:
                    video_service.delete(filename)

        for session in transcode_session.keys():
            status = transcode_session.get(session)
            if isinstance(status, int):
                continue

            timestamp = status.split(' ')[1]
            time_finished = datetime.fromtimestamp(int(timestamp))

            if current_time - time_finished > Session.TRANSCODE_STATUS_EXPIRES:
                transcode_session.delete(session)

        sleep(
            Session.UPLOAD_CLEANER_SLEEP
        )


cleaner = Thread(
    target = remove_inactive_sessions, 
    daemon = True
)

cleaner.start()
