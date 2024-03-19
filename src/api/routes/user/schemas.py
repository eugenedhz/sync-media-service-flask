from marshmallow import fields

from src.configs.constants import Regex
from src.api.schemas_config import JsonSchema, Length, Range, Regexp


class UserSchema(JsonSchema):
	id = fields.Int(required=False)
	username = fields.Str(required=False)
	registrationDate = fields.Int(required=False)
	email = fields.Email(required=False)
	displayName = fields.Str(required=False)
	isBanned = fields.Boolean(required=False)
	birthday = fields.Int(required=False)
	description = fields.Str(required=False)
	avatar = fields.Str(required=False)


class UpdateUserSchema(JsonSchema):
	username = fields.Str(required=False, validate=[Length(min=5, max=30), Regexp(regex=Regex.USERNAME)])
	email = fields.Email(required=False)
	displayName = fields.Str(required=False, validate=Length(min=1, max=30))
	birthday = fields.Int(required=False, validate=Range(min=86400))
	description = fields.Str(required=False, validate=Length(min=1, max=140))