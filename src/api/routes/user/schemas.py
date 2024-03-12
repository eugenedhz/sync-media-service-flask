from marshmallow import fields

from src.api.schemas_config import JsonSchema, Length


class RegisterSchema(JsonSchema):
	username = fields.Str(required=True,  validate=Length(min=1, max=30))
	displayName = fields.Str(required=True,  validate=Length(min=1, max=30))
	password = fields.Str(required=True, validate=Length(min=1))
	email = fields.Email(required=True, validate=Length(min=1))


class LoginSchema(JsonSchema):
	username = fields.Str(required=True,  validate=Length(min=1, max=30))
	password = fields.Str(required=True, validate=Length(min=1))