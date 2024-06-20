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
    )
}
