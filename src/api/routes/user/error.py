from src.api.error.custom_error import ApiErrorInfo


USER_API_ERRORS = {
	'USERNAME_EXISTS': ApiErrorInfo(
		error_message = 'USERNAME_ALREADY_EXISTS', 
		status_code = 409
	),
	
	'EMAIL_EXISTS': ApiErrorInfo(
		error_message = 'EMAIL_ALREADY_EXISTS', 
		status_code = 409
	),

	'NO_USER_FOUND': ApiErrorInfo(
		error_message = 'NO_USER_FOUND', 
		status_code = 404
	),

	'NO_USERS_FOUND': ApiErrorInfo(
		error_message = 'NO_USERS_FOUND', 
		status_code = 404
	),
}