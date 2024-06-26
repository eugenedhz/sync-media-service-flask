from src.api.error.custom_error import ApiErrorInfo


PLAYLIST_MEDIA_API_ERRORS = {
    'PLAYLIST_MEDIA_NOT_FOUND': ApiErrorInfo(
        error_message = 'PLAYLIST_MEDIA_NOT_FOUND',
        status_code = 404
    ),

    'PLAYLIST_MEDIAS_NOT_FOUND': ApiErrorInfo(
        error_message = 'PLAYLIST_MEDIAS_NOT_FOUND',
        status_code = 404
    ),

    'PLAYLIST_MEDIA_ALREADY_IN_ROOM': ApiErrorInfo(
        error_message = 'PLAYLIST_MEDIA_ALREADY_IN_ROOM',
        status_code = 409
    ),

    'PLAYLIST_ORDER_OUT_OF_RANGE': ApiErrorInfo(
        error_message = 'PLAYLIST_ORDER_OUT_OF_RANGE',
        status_code = 400
    ),

    'SAME_PLAYLIST_MEDIA_ORDER': ApiErrorInfo(
        error_message = 'SAME_PLAYLIST_MEDIA_ORDER',
        status_code = 409
    )
}
