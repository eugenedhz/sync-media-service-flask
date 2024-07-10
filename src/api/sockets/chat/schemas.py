from marshmallow import fields

from src.api.schemas_config import JsonSchema

from pkg.json.validators import Length, Range


class MessageSchema(JsonSchema):
	roomId = fields.Integer(required=True, validate=Range(min=1))
	message = fields.String(required=True, validate=Length(min=1))
