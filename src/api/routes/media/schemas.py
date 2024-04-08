from marshmallow import fields

from src.api.schemas_config import JsonSchema

from pkg.json.validators import Length


class MediaSchema(JsonSchema):
    id = fields.Int(required=False)
    name = fields.Str(required=False)
    description = fields.Str(required=False)
    thumbnail = fields.Str(required=False)
    preview = fields.Str(required=False)
    trailer = fields.Str(required=False)


class UpdateMediaSchema(JsonSchema):
    id = fields.Int(required=False)
    name = fields.Str(required=False)
    description = fields.Str(required=False)


class CreateMediaSchema(JsonSchema):
    name = fields.Str(required=True, validate=[Length(min=1, max=50)])
    description = fields.Str(required=True, validate=[Length(max=200)])


class MediaFilesSchema(JsonSchema):
    thumbnail = fields.Field(required=True)
    preview = fields.Field(required=True)