from marshmallow import Schema, fields, validate
from src.api.error.custom_error import ApiError, ApiErrorInfo


fields.Field.default_error_messages = {
	        "required": "MISSING_FIELD",
	        "null": "NOT_NULLABLE",
	        "validator_failed": "INVALID_VALUE"
}


class Length(validate.Length):
	def __init__(
		self,
		min: int | None = None,
		max: int | None = None,
		*,
		equal: int | None = None,
		error: str | None = None,
	):

		super().__init__(min=min, max=max, equal=equal, error=error)

		self.error = 'INVALID_LENGTH'



class JsonSchema(Schema):

		error_messages = {
	        "unknown": "UNKNOWN_FIELD"
    	}

		def handle_error(self, exc, data, **kwargs):
			invalid_fields = exc.messages

			for key in invalid_fields:
				if 'Not a valid' in invalid_fields[key][0]:
					invalid_fields[key] = 'INVALID_TYPE'
				else:
					invalid_fields[key] = invalid_fields[key][0]

			raise ApiError(
				ApiErrorInfo(
					error_message = invalid_fields, 
					description = "JSON не соответствует схеме, смотрите в swagger."
				)
			)