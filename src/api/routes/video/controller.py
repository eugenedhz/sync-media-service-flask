from datetime import datetime
from uuid import uuid4

from flask import request, jsonify, send_from_directory
from flask_jwt_extended import jwt_required

from src.app import app
from src.configs.constants import Static, VideoUploadSession, Role
from src.api.services.video import video_service, upload_session, transcode_session
from src.api.routes.video.schemas import UploadSchema, ChunkSchema
from src.api.error.custom_error import ApiError
from src.api.error.shared_error import API_ERRORS
from src.api.routes.video.error import VIDEO_API_ERRORS
from src.threads.video.transcoder import transcode_queue
from src.api.helpers.jwt import role_required

from pkg.file.video.validate import is_valid_video_extension
from pkg.file.filename import split_filename


@app.route('/upload/session', methods=['GET'])
@jwt_required()
@role_required(Role.ADMIN)
def get_session():
    current_time = int(datetime.now().timestamp())
    uuid = uuid4().hex
    upload_session.set(uuid, current_time)

    return jsonify(session=uuid)


@app.route('/upload', methods=['POST'])
@jwt_required()
@role_required(Role.ADMIN)
def upload_chunk():
    ChunkSchema().validate(request.files)
    formdata = UploadSchema().load(request.form)

    session = formdata['session']
    if upload_session.get(session) == None:
        raise ApiError(VIDEO_API_ERRORS['UPLOAD_SESSION_NOT_FOUND'])

    chunk = request.files['chunk']
    extension = split_filename(chunk.filename).extension

    if not is_valid_video_extension(extension):
        raise ApiError(API_ERRORS['INVALID_VIDEO'])

    filename = session + extension
    index = formdata['chunkIndex']
    last_index = formdata['totalChunkCount'] - 1
    total_size = formdata['totalFileSize']
    offset = formdata['chunkByteOffset']
    data = chunk.read()

    try:
        video_service.write_chunk(
            data = data, 
            chunk_offset = offset, 
            filename = filename
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

    if index != last_index:
        return jsonify(chunkUploaded=index)

    size = video_service.get_size(filename)
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


@app.route('/static/videos/<path:filename>', methods=['GET'])
def get_video(filename):
    quality = request.args.get('quality')

    if quality is None:
        raise ApiError(VIDEO_API_ERRORS['NO_QUALITY_PROVIDED'])

    if not quality in Static.VIDEOS_QUALITIES:
        raise ApiError(VIDEO_API_ERRORS['QUALITY_NOT_FOUND'])

    name, extension = split_filename(filename)
    filename = f'{ name }{ quality }{ extension }'

    try:
        return send_from_directory(Static.VIDEOS_URL[1:-1], filename)
    except:
        raise ApiError(VIDEO_API_ERRORS['VIDEO_NOT_FOUND'])


@app.route('/upload/session', methods=['DELETE'])
@jwt_required()
@role_required(Role.ADMIN)
def abort_upload():
    session = request.args.get('session')

    if session is None:
        raise ApiError(VIDEO_API_ERRORS['NO_UPLOAD_SESSION_PROVIDED'])

    if upload_session.get(session) is None:
        raise ApiError(VIDEO_API_ERRORS['UPLOAD_SESSION_NOT_FOUND'])

    upload_session.delete(session)
    filename = video_service.find(session)

    if filename != None:
        video_service.delete(filename)

    return jsonify(aborted=session)


@app.route('/upload/transcode_status', methods=['GET'])
def get_transcode_statuses():
    session = request.args.get('session')

    if session is None:
        raise ApiError(VIDEO_API_ERRORS['NO_UPLOAD_SESSION_PROVIDED'])

    statuses = dict()

    for quality in Static.VIDEOS_QUALITIES:
        status = transcode_session.get(session+quality)
        if isinstance(status, str):
            status = int(status.split()[0])

        statuses[quality] = VideoUploadSession.TRANSCODE_STATUSES[status]

    for quality in statuses:
        if statuses[quality] != VideoUploadSession.TRANSCODE_STATUSES[None]:
            return jsonify(statuses)

    raise ApiError(VIDEO_API_ERRORS['TRANSCODE_SESSION_NOT_FOUND'])
