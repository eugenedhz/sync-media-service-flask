from marshmallow import fields

from src.api.schemas_config import JsonSchema
from src.configs.constants import Regex

from pkg.json.validators import Length, Regexp

class GenreSchema(JsonSchema):
    id = fields.Integer()
    name = fields.String()
    slug = fields.String() 