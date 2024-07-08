from src.api.error.custom_error import ApiErrorInfo
from src.configs.constants import Role


API_ERRORS = {
	'INVALID_ID': ApiErrorInfo(
		error_message = 'INVALID_ID', 
		description = 'Incorrect type of entity ID provided.'
	),

	'NO_IDENTITY_PROVIDED': ApiErrorInfo(
		error_message = 'NO_IDENTITY_PROVIDED',
		description = 'No identifier of entity in query parameters to search with.'
	),

	'EMPTY_FORMDATA': ApiErrorInfo(
		error_message = 'FORMDATA_IS_EMPTY',
		description = 'Formdata must contain at least one field.'
	),

	'INVALID_JPG': ApiErrorInfo(
		error_message = 'INVALID_JPG',
		description = 'Image must be valid .jpg format.'
	),
	
	'INVALID_VIDEO': ApiErrorInfo(
		error_message = 'INVALID_VIDEO',
		description = 'Video must be .mp4, .mov, .avi or .m4v format.'
	),

	'CANT_SAVE_FILE': ApiErrorInfo(
		error_message = 'CANNOT_SAVE_FILE_ON_SERVER',
		description = 'Due to some system errors it was unable to save file on the server.',
		status_code = 500
	),

	'INVALID_FILTERS': ApiErrorInfo(
		error_message = 'INVALID_FILTER_BY',
		description = 'Check if fields and their value type match requesting entity.',
		status_code = 400
	),

	'INVALID_SELECT': ApiErrorInfo(
		error_message = 'INVALID_SELECT',
		description = 'Check if fields match requesting entity.',
		status_code = 400
	),

	'INVALID_EXPAND': ApiErrorInfo(
		error_message = 'INVALID_EXPAND',
		description = 'Check if fields match requesting entity.',
		status_code = 400
	),

	'INVALID_PAGE_QUERY': ApiErrorInfo(
		error_message = 'INVALID_PAGE_QUERY',
		status_code = 400
	),

	f'{Role.ADMIN}_RIGHTS_REQUIRED': ApiErrorInfo(
		error_message = f'{Role.ADMIN}_RIGHTS_REQUIRED',
		status_code = 403
	),

	'USER_SOCKET_SESSION_NOT_FOUND': ApiErrorInfo(
		error_message = 'USER_SOCKET_SESSION_NOT_FOUND',
		description = 'You must connect to sockets to do this.',
		status_code = 404
	),
}