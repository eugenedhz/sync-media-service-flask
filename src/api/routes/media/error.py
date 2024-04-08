from src.api.error.custom_error import ApiErrorInfo

MEDIA_API_ERRORS = {
    'MEDIA_EXISTS': ApiErrorInfo(
        error_message = 'MEDIA_ALREADY_EXISTS',
        status_code = 409
    ),

    'MEDIA_NOT_FOUND': ApiErrorInfo(
        error_message = 'MEDIA_NOT_FOUND',
        status_code = 404
    ),

    'THUMBNAIL_NOT_PROVIDED': ApiErrorInfo(
        error_message = 'THUMBNAIL_NOT_PROVIDED',
        status_code = 400
    ),

    'PREVIEW_NOT_PROVIDED': ApiErrorInfo(
        error_message = 'PREVIEW_NOT_PROVIDED',
        status_code = 400
    ),
}