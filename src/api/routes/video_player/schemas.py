from marshmallow import fields

from src.api.schemas_config import JsonSchema

from pkg.json.validators import Length, Range, Regexp


class VideoPlayerStateSchema(JsonSchema):
	currentTime = fields.Int(required=True, validate=Range(min=0))
	isPaused = fields.Boolean(required=True)