from marshmallow import Schema, fields

from src.api.error.custom_error import ApiError, ApiErrorInfo


fields.Field.default_error_messages = {
	"required": "MISSING_FIELD",
	"null": "NOT_NULLABLE",
	"validator_failed": "INVALID_VALUE"
}


class JsonSchema(Schema):
	error_messages = {
        "unknown": "UNKNOWN_FIELD"
	}

	def handle_error(self, exc, data, **kwargs):
		invalid_fields = exc.messages
		validation_errors = []

		for key in invalid_fields:
			if 'Not a valid' in invalid_fields[key][0]:
				message = 'INVALID_TYPE'
			else:
				message = invalid_fields[key][0]

			error = ApiErrorInfo(
				error_message = message, 
				field_name = key
			)
			validation_errors.append(error)

		raise ApiError(validation_errors)
