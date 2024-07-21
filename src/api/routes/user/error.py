from src.api.error.custom_error import ApiErrorInfo


USER_API_ERRORS = {
	'USERNAME_EXISTS': ApiErrorInfo(
		error_message = 'USERNAME_ALREADY_EXISTS', 
		field_name = 'username',
		status_code = 409
	),
	
	'EMAIL_EXISTS': ApiErrorInfo(
		error_message = 'EMAIL_ALREADY_EXISTS', 
		field_name = 'email',
		status_code = 409
	),

	'USER_NOT_FOUND': ApiErrorInfo(
		error_message = 'USER_NOT_FOUND', 
		status_code = 404
	),

	'USERS_NOT_FOUND': ApiErrorInfo(
		error_message = 'USERS_NOT_FOUND', 
		status_code = 404
	),
}