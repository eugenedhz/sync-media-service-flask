from marshmallow import fields

from src.api.schemas_config import JsonSchema, CustomLength


class AuthSchema(JsonSchema):
	
	username = fields.Str(required=True,  validate=CustomLength(min=1, max=20))
	password = fields.Str(required=True, validate=CustomLength(min=1, max=200))
	email = fields.Str(required=False)