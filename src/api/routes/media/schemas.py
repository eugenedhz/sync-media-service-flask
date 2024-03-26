from marshmallow import fields

from src.api.schemas_config import JsonSchema


class MediaSchema(JsonSchema):
    mId = fields.Int(required=False)
    mName = fields.Str(required=False)
    description = fields.Str(required=False)
    thumbnail = fields.Str(required=False)
    preview = fields.Str(required=False)
    ratingId = fields.Int(required=False)
    trailer = fields.Int(required=False)
    subtitleId = fields.Int(required=False)
    genreId = fields.Int(required=False)


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