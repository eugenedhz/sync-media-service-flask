from src.api.error.custom_error import ApiErrorInfo


ROOM_SOCKET_ERRORS = {
	'ROOM_NOT_FOUND': ApiErrorInfo(
		error_message = 'ROOM_NOT_FOUND',
	),

	'USER_ALREADY_IN_SOME_ROOM': ApiErrorInfo(
		error_message = 'USER_ALREADY_IN_SOME_ROOM',
		description = 'The user already in some room.'
	),

	'USER_NOT_IN_ROOM': ApiErrorInfo(
		error_message = 'USER_NOT_IN_ROOM'
	),
}