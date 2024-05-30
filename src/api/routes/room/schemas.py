from marshmallow import fields

from src.api.schemas_config import JsonSchema
from src.configs.constants import Regex

from pkg.json.validators import Length, Regexp


class RoomSchema(JsonSchema):
	id = fields.Integer()
	creatorId = fields.Integer()
	name = fields.String()
	title = fields.String()
	isPrivate = fields.Boolean()
	cover = fields.String()


class CreateRoomSchema(JsonSchema):
	name = fields.String(required=True, validate=[Regexp(regex=Regex.ROOM_NAME), Length(min=1, max=30)])
	title = fields.String(required=True, validate=Length(min=1, max=30))
	isPrivate = fields.Boolean(required=True)


class UpdateRoomSchema(JsonSchema):
	name = fields.String(required=False, validate=[Regexp(regex=Regex.ROOM_NAME), Length(min=1, max=30)])
	title = fields.String(required=False, validate=Length(min=1, max=30))
	isPrivate = fields.Boolean(required=False)


class RoomFilesSchema(JsonSchema):
	cover = fields.Field(required=False)
