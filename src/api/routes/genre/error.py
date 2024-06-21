from src.api.error.custom_error import ApiErrorInfo


GENRE_API_ERRORS = {
    'GENRE_NOT_FOUND': ApiErrorInfo(
        error_message = 'GENRE_NOT_FOUND',
        status_code = 404
    ),

    'GENRES_NOT_FOUND': ApiErrorInfo(
        error_message = 'GENRES_NOT_FOUND',
        status_code = 404
    ),

    'SLUG_EXISTS': ApiErrorInfo(
        error_message = 'SLUG_ALREADY_EXISTS',
        status_code = 409
    ),

    'MEDIA_GENRE_EXISTS': ApiErrorInfo(
        error_message = 'MEDIA_GENRE_ALREADY_EXISTS',
        status_code = 409
    ),

    'MEDIA_GENRE_NOT_FOUND': ApiErrorInfo(
        error_message = 'MEDIA_GENRE_NOT_FOUND',
        status_code = 404
    ),

    'MEDIA_GENRES_NOT_FOUND': ApiErrorInfo(
        error_message = 'MEDIA_GENRES_NOT_FOUND',
        status_code = 404
    )
}
 