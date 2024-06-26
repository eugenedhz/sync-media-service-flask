from marshmallow import fields

from src.api.schemas_config import JsonSchema


class PlaylistMediaSchema(JsonSchema):
	id = fields.Integer()
	roomId = fields.Integer()
	mediaId = fields.Integer()
	order = fields.Integer()
	name = fields.String()
	thumbnail = fields.String()