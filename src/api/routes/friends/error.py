from src.api.error.custom_error import ApiErrorInfo


FRIENDS_API_ERRORS = {
    'CANNOT_ADD_YOURSELF': ApiErrorInfo(
        error_message = 'CANNOT_ADD_YOURSELF',
        status_code = 403
    ),

}