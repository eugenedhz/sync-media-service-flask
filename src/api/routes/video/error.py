from src.api.error.custom_error import ApiErrorInfo


VIDEO_API_ERRORS = {
	'UPLOAD_SESSION_NOT_FOUND': ApiErrorInfo(
		error_message = 'UPLOAD_SESSION_NOT_FOUND',
		status_code = 404,
		description = 'Get the session uuid first via /upload/session (GET method).'
	),

	'TRANSCODE_SESSION_NOT_FOUND': ApiErrorInfo(
		error_message = 'TRANSCODE_SESSION_NOT_FOUND',
		status_code = 404,
		description = 'Transcoding might not be started or transcoding already finished.'
	),

	'NO_UPLOAD_SESSION_PROVIDED': ApiErrorInfo(
		error_message = 'NO_UPLOAD_SESSION_PROVIDED',
		status_code = 400
	),
	
	'SIZE_MISMATCH': ApiErrorInfo(
		error_message = 'FILE_TOTAL_SIZE_MISMATCH',
		status_code = 409,
		description = 'File uploaded with chunks has different size to initial file size.'
	),

	'VIDEO_NOT_FOUND': ApiErrorInfo(
		error_message = 'VIDEO_NOT_FOUND',
		status_code = 404
	),

	'NO_QUALITY_PROVIDED': ApiErrorInfo(
		error_message = 'NO_QUALITY_PROVIDED',
		status_code = 400
	),

	'QUALITY_NOT_FOUND': ApiErrorInfo(
		error_message = 'QUALITY_NOT_FOUND',
		status_code = 404
	),
}