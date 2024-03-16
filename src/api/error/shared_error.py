from src.api.error.custom_error import ApiErrorInfo


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
}