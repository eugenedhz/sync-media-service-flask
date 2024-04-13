from marshmallow import fields

from src.api.schemas_config import JsonSchema
from src.configs.constants import Regex

from pkg.json.validators import Length, Regexp


class MediaSchema(JsonSchema):
    id = fields.Integer()
    name = fields.String()
    description = fields.String()
    thumbnail = fields.String()
    preview = fields.String()
    trailer = fields.String()


class UpdateMediaSchema(JsonSchema):
    name = fields.Str(required=False, validate=Length(min=1, max=50))
    description = fields.Str(required=False, validate=Length(max=200))
    trailer = fields.Str(required=False, validate=Regexp(regex=Regex.TRAILER))


class CreateMediaSchema(JsonSchema):
    name = fields.Str(required=True, validate=Length(min=1, max=50))
    description = fields.Str(required=True, validate=Length(max=200))
    trailer = fields.Str(required=False, validate=Regexp(regex=Regex.TRAILER))


class CreateUpdateMediaFilesSchema(JsonSchema):
    thumbnail = fields.Field(required=True)
    preview = fields.Field(required=True)


class UpdateMediaFilesSchema(JsonSchema):
    thumbnail = fields.Field(required=False)
    preview = fields.Field(required=False)
