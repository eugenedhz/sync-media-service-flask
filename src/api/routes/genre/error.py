from src.api.error.custom_error import ApiErrorInfo

GENRE_API_ERRORS = {
    'GENRE_NOT_FOUND': ApiErrorInfo(
        error_message = 'GENRE_NOT_FOUND',
        status_code = 404
    ),

    'GENRES_NOT_FOUND': ApiErrorInfo(
        error_message='GENRES_NOT_FOUND',
        status_code=404
    ),
}
