from flask import request, jsonify

from src.app import app
from src.domain.participant import Participant
from src.api.services.participant import participant_service
from src.api.routes.participant.schemas import ParticipantSchema
from src.usecase.participant.dto import ParticipantDTO
from src.usecase.dto import QueryParametersDTO
from src.api.error.shared_error import API_ERRORS
from src.api.routes.participant.error import PARTICIPANT_API_ERRORS
from src.api.error.custom_error import ApiError

from pkg.query_params.select.parse import parse_select
from pkg.query_params.filter_by.parse import parse_filter_by


@app.route('/participants', methods=['GET'])
def get_participant_by_id():
    request_params = request.args

    participant_id = request_params.get('id')

    if participant_id is None:
        raise ApiError(API_ERRORS['NO_IDENTITY_PROVIDED'])

    select = request_params.get('select')
    participant_fields = ParticipantDTO.__match_args__
    try:
        select = parse_select(select=select, valid_fields=participant_fields)
    except:
        raise ApiError(API_ERRORS['INVALID_SELECT'])

    participant = participant_service.get_participant_by_id(participant_id)

    if participant is None:
        raise ApiError(PARTICIPANT_API_ERRORS['PARTICIPANT_NOT_FOUND'])

    serialize_participant = ParticipantSchema(only=select).dump
    serialized_participant = serialize_participant(participant)

    return jsonify(serialized_participant)


@app.route('/participants/all', methods=['GET'])
def get_all_participants():
    request_params = request.args

    select = request_params.get('select')
    filter_by = request_params.get('filter_by')

    participant_fields = ParticipantDTO.__match_args__
    try:
        select = parse_select(select=select, valid_fields=participant_fields)
    except:
        raise ApiError(API_ERRORS['INVALID_SELECT'])

    participant_fields = Participant.__annotations__
    try:
        filter_by = parse_filter_by(filter_query=filter_by, valid_fields=participant_fields)
    except:
        raise ApiError(API_ERRORS['INVALID_FILTERS'])

    limit = request_params.get('limit')
    offset = request_params.get('offset')
    if limit or offset:
        try:
            limit = int(limit)
            offset = int(offset)
        except:
            raise ApiError(API_ERRORS['INVALID_PAGE_QUERY'])

    query_parameters_dto = QueryParametersDTO(filters=filter_by, limit=limit, offset=offset)
    participants = participant_service.get_participants(query_parameters_dto=query_parameters_dto)

    if len(participants) == 0:
        return jsonify([])

    serialize_participants = ParticipantSchema(only=select, many=True).dump
    serialized_participants = serialize_participants(participants)

    return jsonify(serialized_participants)
