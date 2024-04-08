from marshmallow import fields

from src.api.schemas_config import JsonSchema

from pkg.json.validators import Length


class MediaSchema(JsonSchema):
    id = fields.Int(required=False)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    thumbnail = fields.Str(required=True)
    preview = fields.Str(required=True)
    trailer = fields.Str(required=False)


class UpdateMediaSchema(JsonSchema):
    id = fields.Int(required=False)
    name = fields.Str(required=True, validate=[Length(min=1, max=50)])
    description = fields.Str(required=True, validate=[Length(max=200)])


class CreateMediaSchema(JsonSchema):
    name = fields.Str(required=True, validate=[Length(min=1, max=50)])
    description = fields.Str(required=True, validate=[Length(max=200)])


class MediaFilesSchema(JsonSchema):
    thumbnail = fields.Field(required=True)
    preview = fields.Field(required=True)