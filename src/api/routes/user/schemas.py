from marshmallow import fields

from src.api.schemas_config import JsonSchema, Length


class UserSchema(JsonSchema):
	id = fields.Int(required=False)
	username = fields.Str(required=False)
	registrationDate = fields.Int(required=False)
	email = fields.Str(required=False)
	displayName = fields.Str(required=False)
	isBanned = fields.Boolean(required=False)
	birthday = fields.Int(required=False)
	description = fields.Str(required=False)
	avatar = fields.Str(required=False)


class UpdateUserSchema(JsonSchema):
	username = fields.Str(required=False)
	email = fields.Str(required=False)
	displayName = fields.Str(required=False)
	birthday = fields.Int(required=False)
	description = fields.Str(required=False)


class RegisterSchema(JsonSchema):
	username = fields.Str(required=True,  validate=Length(min=1, max=30))
	displayName = fields.Str(required=True,  validate=Length(min=1, max=30))
	password = fields.Str(required=True, validate=Length(min=1))
	email = fields.Email(required=True, validate=Length(min=1))


class LoginSchema(JsonSchema):
	username = fields.Str(required=True,  validate=Length(min=1, max=30))
	password = fields.Str(required=True, validate=Length(min=1))
