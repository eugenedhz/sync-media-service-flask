from marshmallow import fields

from src.configs.constants import Regex
from src.api.schemas_config import JsonSchema, Length, Regexp


class RegisterSchema(JsonSchema):
	username = fields.Str(required=True,  validate=[Length(min=5, max=30), Regexp(regex=Regex.USERNAME)])
	displayName = fields.Str(required=True,  validate=Length(min=1, max=30))
	password = fields.Str(required=True, validate=[Length(min=8), Regexp(regex=Regex.PASSWORD)])
	email = fields.Email(required=True)


class LoginSchema(JsonSchema):
	username = fields.Str(required=True,  validate=[Length(min=5, max=30), Regexp(regex=Regex.USERNAME)])
	password = fields.Str(required=True, validate=[Length(min=8), Regexp(regex=Regex.PASSWORD)])
