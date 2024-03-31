from marshmallow import fields

from src.api.schemas_config import JsonSchema


class MediaSchema(JsonSchema):
    id = fields.Int(required=False)
    name = fields.Str(required=False)
    description = fields.Str(required=False)
    thumbnail = fields.Str(required=False)
    preview = fields.Str(required=False)
    trailer = fields.Str(required=False)


class UpdateMediaSchema(JsonSchema):
    name = fields.Str(required=False)
    description = fields.Str(required=False)
    thumbnail = fields.Str(required=False)
    preview = fields.Str(required=False)


class CreateMediaSchema(JsonSchema):
    name = fields.Str(required=False)
    description = fields.Str(required=False)
    thumbnail = fields.Str(required=False)
    preview = fields.Str(required=False)