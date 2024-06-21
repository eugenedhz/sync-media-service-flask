from marshmallow import fields

from src.api.schemas_config import JsonSchema

from pkg.json.validators import Range


class PlaylistMediaSchema(JsonSchema):
	id = fields.Integer()
	roomId = fields.Integer()
	mediaId = fields.Integer()
	order = fields.Integer()
	name = fields.String()
	thumbnail = fields.String()


class CreatePlaylistMediaSchema(JsonSchema):
	roomId = fields.Integer(required=True, validate=Range(min=1))
	mediaId = fields.Integer(required=True, validate=Range(min=1))


class UpdatePlaylistMediaSchema(JsonSchema):
	order = fields.Integer(required=True, validate=Range(min=0))
