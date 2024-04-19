from src.api.error.custom_error import ApiErrorInfo


MEDIA_API_ERRORS = {
    'MEDIA_NOT_FOUND': ApiErrorInfo(
        error_message = 'MEDIA_NOT_FOUND',
        status_code = 404
    ),

    'MEDIAS_NOT_FOUND': ApiErrorInfo(
        error_message='MEDIAS_NOT_FOUND',
        status_code=404
    ),
}
