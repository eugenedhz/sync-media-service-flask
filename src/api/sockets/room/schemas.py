from marshmallow import fields

from src.api.schemas_config import JsonSchema

from pkg.json.validators import Range


class JoinAndLeaveRoomSchema(JsonSchema):
	roomId = fields.Integer(required=True, validate=Range(min=1))
