from src.api.error.custom_error import ApiErrorInfo


PARTICIPANT_API_ERRORS = {
    'PARTICIPANT_NOT_FOUND': ApiErrorInfo(
        error_message = 'PARTICIPANT_NOT_FOUND',
        status_code = 404
    ),

    'PARTICIPANTS_NOT_FOUND': ApiErrorInfo(
        error_message = 'PARTICIPANTS_NOT_FOUND',
        status_code = 404
    )
}
