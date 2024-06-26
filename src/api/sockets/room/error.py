from src.api.error.custom_error import ApiErrorInfo


ROOM_SOCKET_ERRORS = {
	'ROOM_NOT_FOUND': ApiErrorInfo(
		error_message = 'ROOM_NOT_FOUND',
	),

	'ALREADY_PARTICIPANTING': ApiErrorInfo(
		error_message = 'ALREADY_PARTICIPANTING',
		description = 'The user already in some room.'
	),

	'PARTICIPANT_NOT_IN_ROOM': ApiErrorInfo(
		error_message = 'PARTICIPANT_NOT_IN_ROOM',
		description = 'Cannot leave room in which user is not participanting.'
	),
}