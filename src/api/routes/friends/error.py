from src.api.error.custom_error import ApiErrorInfo


FRIENDS_API_ERRORS = {
    'CANNOT_ADD_YOURSELF': ApiErrorInfo(
        error_message = 'CANNOT_ADD_YOURSELF',
        status_code = 403
    ),

    'ALREADY_REQUESTED': ApiErrorInfo(
        error_message = 'ALREADY_REQUESTED',
        status_code = 403
    ),

    'FRIEND_NOT_FOUND': ApiErrorInfo(
        error_message = 'FRIEND_NOT_FOUND',
        status_code = 404
    ),

    'FRIENDS_NOT_FOUND': ApiErrorInfo(
        error_message = 'FRIENDS_NOT_FOUND',
        status_code = 404
    ),

    'REQUEST_NOT_FOUND': ApiErrorInfo(
        error_message = 'REQUEST_NOT_FOUND',
        status_code = 404
    ),

}