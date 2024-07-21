from src.api.error.custom_error import ApiErrorInfo


MEDIA_VIDEO_API_ERRORS = {
    'MEDIA_VIDEO_NOT_FOUND': ApiErrorInfo(
        error_message = 'MEDIA_VIDEO_NOT_FOUND',
        status_code = 404
    ),

    'MEDIA_VIDEOS_NOT_FOUND': ApiErrorInfo(
        error_message = 'MEDIA_VIDEOS_NOT_FOUND',
        status_code = 404
    ),

    'SOURCE_EXISTS': ApiErrorInfo(
        error_message = 'MEDIA_VIDEO_SOURCE_ALREADY_EXISTS',
        field_name = 'source',
        status_code = 409
    ),

    'LANGUAGE_NOT_FOUND': ApiErrorInfo(
        error_message = 'LANGUAGE_NOT_FOUND',
        field_name = 'language',
        status_code = 404,
        description = 'Check for correct country code for the language.'
    ),
}
