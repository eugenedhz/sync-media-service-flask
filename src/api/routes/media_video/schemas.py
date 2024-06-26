from marshmallow import fields

from src.api.schemas_config import JsonSchema
from src.configs.constants import Regex

from pkg.json.validators import Regexp, Range, Length


class MediaVideoSchema(JsonSchema):
	id = fields.Integer()
	mediaId = fields.Integer()
	name = fields.String()
	source = fields.String()
	language = fields.String()


class CreateMediaVideoSchema(JsonSchema):
	mediaId = fields.Int(required=True, validate=Range(min=1))
	name = fields.String(required=True, validate=Length(min=1))
	source = fields.String(required=True, validate=Regexp(regex=Regex.VIDEO))
	language = fields.String(required=True, validate=Regexp(regex=Regex.COUNTRY_CODE))


class UpdateMediaVideoSchema(JsonSchema):
	name = fields.String(required=False, validate=Length(min=1))
	source = fields.String(required=False, validate=Regexp(regex=Regex.VIDEO))
	language = fields.String(required=False, validate=Regexp(regex=Regex.COUNTRY_CODE))
