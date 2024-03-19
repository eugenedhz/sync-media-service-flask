from src.api.error.custom_error import ApiErrorInfo


AUTH_API_ERRORS = {
	'USERNAME_EXISTS': ApiErrorInfo(
		error_message = 'USERNAME_ALREADY_EXISTS', 
		status_code = 409
	),
	
	'EMAIL_EXISTS': ApiErrorInfo(
		error_message = 'EMAIL_ALREADY_EXISTS', 
		status_code = 409
	),

	'USERNAME_NO_EXIST': ApiErrorInfo(
		error_message = 'USERNAME_DOESNT_EXIST', 
		status_code = 409
	),

	'WRONG_PWD': ApiErrorInfo(
		error_message = 'INCORRECT_PASSWORD', 
		status_code = 409
	),

	'BANNED': ApiErrorInfo(
		error_message = 'USER_IS_BANNED', 
		status_code = 403
	)
}