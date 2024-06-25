from marshmallow import fields

from src.api.schemas_config import JsonSchema


class ParticipantSchema(JsonSchema):
	id = fields.Integer()
	roomId = fields.Integer()
	userId = fields.Integer()
	name = fields.String()
	avatar = fields.String()
