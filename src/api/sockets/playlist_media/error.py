from src.api.error.custom_error import ApiErrorInfo


PLAYLIST_MEDIA_SOCKET_ERRORS = {
    'PLAYLIST_MEDIA_NOT_FOUND': ApiErrorInfo(
        error_message = 'PLAYLIST_MEDIA_NOT_FOUND'
    ),

    'PLAYLIST_MEDIA_ALREADY_IN_ROOM': ApiErrorInfo(
        error_message = 'PLAYLIST_MEDIA_ALREADY_IN_ROOM'
    ),

    'PLAYLIST_ORDER_OUT_OF_RANGE': ApiErrorInfo(
        error_message = 'PLAYLIST_ORDER_OUT_OF_RANGE'
    ),

    'SAME_PLAYLIST_MEDIA_ORDER': ApiErrorInfo(
        error_message = 'SAME_PLAYLIST_MEDIA_ORDER'
    ),

    'PLAYLIST_MEDIA_ALREADY_IN_PLAYER': ApiErrorInfo(
        error_message = 'PLAYLIST_MEDIA_ALREADY_IN_PLAYER'
    )
}
