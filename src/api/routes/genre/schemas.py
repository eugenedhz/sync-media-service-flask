from marshmallow import fields

from src.api.schemas_config import JsonSchema
from src.configs.constants import Regex

from pkg.json.validators import Length, Regexp, Range


class GenreSchema(JsonSchema):
    id = fields.Integer()
    name = fields.String()
    slug = fields.String() 


class UpdateGenreSchema(JsonSchema):
    slug = fields.String(required=False, validate=[Length(min=2), Regexp(regex=Regex.GENRE_SLUG)])     
    name = fields.String(required=False, validate=[Length(min=2), Regexp(regex=Regex.GENRE_NAME)])


class CreateGenreSchema(JsonSchema):
    slug = fields.String(required=True, validate=[Length(min=2), Regexp(regex=Regex.GENRE_SLUG)]) 
    name = fields.String(required=True, validate=[Length(min=2), Regexp(regex=Regex.GENRE_NAME)])


class GenreAddOrDeleteFromMediaSchema(JsonSchema):
    mediaId = fields.Integer(required=True, validate=Range(min=1))
    genreId = fields.Integer(required=True, validate=Range(min=1))