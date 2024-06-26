from marshmallow import fields

from src.api.schemas_config import JsonSchema

from pkg.json.validators import Range, Length


class PlayerStateSyncWithUserSchema(JsonSchema):
	userSID = fields.String(required=True, validate=Length(min=1))
	currentTime = fields.Int(required=True, validate=Range(min=0))
	isPaused = fields.Boolean(required=True)


class PlayerStateSyncWithEveryoneSchema(JsonSchema):
	roomId = fields.Int(required=True, validate=Range(min=1))
	currentTime = fields.Int(required=True, validate=Range(min=0))
	isPaused = fields.Boolean(required=True)


class PlayerStateRequestSchema(JsonSchema):
	roomId = fields.Int(required=True, validate=Range(min=1))
