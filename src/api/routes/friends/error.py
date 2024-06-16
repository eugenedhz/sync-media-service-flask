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

    'FRIEND_DOES_NOT_EXIST': ApiErrorInfo(
        error_message = 'FRIEND_DOES_NOT_EXIST',
        status_code = 404
    ),

    'REQUEST_DOES_NOT_EXIST': ApiErrorInfo(
        error_message = 'REQUEST_DOES_NOT_EXIST',
        status_code = 404
    ),

}