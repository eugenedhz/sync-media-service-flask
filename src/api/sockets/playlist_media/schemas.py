from marshmallow import fields

from src.api.schemas_config import JsonSchema

from pkg.json.validators import Range


class CreatePlaylistMediaSchema(JsonSchema):
	roomId = fields.Integer(required=True, validate=Range(min=1))
	mediaId = fields.Integer(required=True, validate=Range(min=1))


class UpdatePlaylistMediaSchema(JsonSchema):
	playlistMediaId = fields.Integer(required=True, validate=Range(min=1))
	order = fields.Integer(required=True, validate=Range(min=1))


class PlaylistMediaIdSchema(JsonSchema):
	playlistMediaId = fields.Integer(required=True, validate=Range(min=1))
