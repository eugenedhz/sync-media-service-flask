from marshmallow import fields

from src.api.schemas_config import JsonSchema


class GenreSchema(JsonSchema):
    id = fields.Integer()
    name = fields.String()
    slug = fields.String() 



class UpdateGenreSchema(JsonSchema):
    slug = fields.String(required=True)     
    name = fields.String(required=False)


class CreateGenreSchema(JsonSchema):
    name = fields.String(required=True)
    slug = fields.String(required=True) 