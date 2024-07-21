from src.api.error.custom_error import ApiErrorInfo


ROOM_API_ERRORS = {
    'ROOM_NOT_FOUND': ApiErrorInfo(
        error_message = 'ROOM_NOT_FOUND',
        status_code = 404
    ),

    'ROOMS_NOT_FOUND': ApiErrorInfo(
        error_message = 'ROOMS_NOT_FOUND',
        status_code = 404
    ),

    'ROOM_NAME_EXISTS': ApiErrorInfo(
        error_message = 'ROOM_NAME_ALREADY_EXISTS',
        field_name = 'name',
        status_code = 409
    ),

    'CREATOR_RIGHTS_REQUIRED': ApiErrorInfo(
        error_message = 'CREATOR_RIGHTS_REQUIRED',
        status_code = 403
    ),
}
