from datetime import datetime
from uuid import uuid4

from flask import request, jsonify, send_from_directory
from flask_jwt_extended import jwt_required
from werkzeug import secure_filename

from src.app import app
from src.configs.constants import Static, Session
from src.api.services.video import video_service, upload_session, transcode_session
from src.api.routes.video.schemas import UploadSchema, ChunkSchema
from src.threads.video.transcoder import transcode_queue
from src.api.error.custom_error import ApiError
from src.api.error.shared_error import API_ERRORS
from src.api.routes.video.error import VIDEO_API_ERRORS

from pkg.file.video.video_validate import is_valid_video
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

        transcode_queue.put_nowait((size, filename))
        return jsonify(video=filename)

    return jsonify(chunk_uploaded=index)


@app.route('/static/videos/<path:filename>', methods=['GET'])
def get_video(filename):
    quality = request.args.get('quality')

    filename = secure_filename(filename) # убирает ненужные слеши и пути, санитайзер по сути
    name, extension = filename.split('.')
    filename = f'{ name }{ quality }.{ extension }'

    return send_from_directory('static/videos', filename)


@app.route('/upload', methods=['DELETE'])
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
    upload_session = request.args.get('session')

    if session is None:
        raise ApiError(VIDEO_API_ERRORS['UPLOAD_SESSION_NOT_PROVIDED'])

    statuses = dict()
    qualities = Static.VIDEO_SIZES.keys()
    first_session = upload_session + qualities[0]

    if transcode_session.get(first_session) is None:
        raise ApiError(VIDEO_API_ERRORS['TRANSCODE_SESSION_NOT_FOUND'])

    for quality in qualities:
        status = transcode_session.get(upload_session+quality)
        if isinstance(status, str):
            status = int(status.split()[0])

        statuses[quality] = Session.TRANSCODE_STATUSES[status]

    return jsonify(statuses)