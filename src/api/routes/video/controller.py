from datetime import datetime
from uuid import uuid4

from flask import request, jsonify, send_from_directory
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename

from src.app import app
from src.configs.constants import Static, Session
from src.api.services.video import video_service, upload_session, transcode_session
from src.api.routes.video.schemas import UploadSchema, ChunkSchema
from src.api.error.custom_error import ApiError
from src.api.error.shared_error import API_ERRORS
from src.api.routes.video.error import VIDEO_API_ERRORS
from src.threads.video.transcoder import transcode_queue

from pkg.file.video.validate import is_valid_video
from pkg.file.filename import get_extension


@app.route('/upload/session', methods=['GET'])
def get_session():
    current_time = int(datetime.now().timestamp())
    uuid = uuid4().hex
    upload_session.set(uuid, current_time)

    return jsonify(session=uuid)


@app.route('/upload', methods=['POST'])
def upload_chunk():
    ChunkSchema().validate(request.files)
    formdata = UploadSchema().load(request.form)

    session = formdata['session']
    if upload_session.get(session) == None:
        raise ApiError(VIDEO_API_ERRORS['UPLOAD_SESSION_NOT_FOUND'])

    chunk = request.files['chunk']
    extension = get_extension(chunk.filename)

    if not is_valid_video(extension):
        raise ApiError(API_ERRORS['INVALID_VIDEO'])

    filename = session + extension
    index = formdata['chunkIndex']
    last_index = formdata['totalChunkCount'] - 1
    total_size = formdata['totalFileSize']
    offset = formdata['chunkByteOffset']
    data = chunk.read()

    try:
        video_service.write_chunk(
            data=data, 
            chunk_offset=offset, 
            filename=filename
        )
    except:
        try:
            video_service.delete(filename)
        except:
            pass

        upload_session.delete(session)
        raise ApiError(API_ERRORS['CANT_SAVE_FILE'])

    current_time = int(datetime.now().timestamp())
    upload_session.set(session, current_time)

    if index == last_index:
        size = video_service.file_size(filename)
        upload_session.delete(session)

        if total_size != size:
            try:
                video_service.delete(filename)
            except:
                pass

            raise ApiError(VIDEO_API_ERRORS['SIZE_MISMATCH'])

        for quality in Static.VIDEOS_QUALITIES:
            transcode_session.set(session+quality, 3) # значение сессии = 3 эквивалентно статусу [pending]

        transcode_queue.put_nowait((size, filename))

        filename = session + Static.VIDEOS_TRANSCODED_EXTENSION
        return jsonify(video=filename)

    return jsonify(chunkUploaded=index)


@app.route('/static/videos/<path:filename>', methods=['GET'])
def get_video(filename):
    quality = request.args.get('quality')

    if quality is None:
        raise ApiError(VIDEO_API_ERRORS['QUALITY_NOT_PROVIDED'])

    filename = secure_filename(filename) # убирает ненужные слеши и пути, санитайзер по сути
    name, extension = filename.split('.')
    filename = f'{ name }{ quality }.{ extension }'

    try:
        return send_from_directory(Static.VIDEOS_URL[1:-1], filename)
    except:
        raise ApiError(VIDEO_API_ERRORS['VIDEO_NOT_FOUND'])


@app.route('/upload/session', methods=['DELETE'])
def abort_upload():
    session = request.args.get('session')

    if session is None:
        raise ApiError(VIDEO_API_ERRORS['UPLOAD_SESSION_NOT_PROVIDED'])

    if upload_session.get(session) is None:
        raise ApiError(VIDEO_API_ERRORS['UPLOAD_SESSION_NOT_FOUND'])

    upload_session.delete(session)
    filename = video_service.find_file(session)

    if filename != None:
        video_service.delete(filename)

    return jsonify(aborted=session)


@app.route('/upload/transcode_status', methods=['GET'])
def get_transcode_statuses():
    session = request.args.get('session')

    if session is None:
        raise ApiError(VIDEO_API_ERRORS['UPLOAD_SESSION_NOT_PROVIDED'])

    statuses = dict()

    for quality in Static.VIDEOS_QUALITIES:
        status = transcode_session.get(session+quality)
        if isinstance(status, str):
            status = int(status.split()[0])

        statuses[quality] = Session.TRANSCODE_STATUSES[status]

    for quality in statuses:
        if statuses[quality] != Session.TRANSCODE_STATUSES[None]:
            return jsonify(statuses)

    raise ApiError(VIDEO_API_ERRORS['TRANSCODE_SESSION_NOT_FOUND'])
