from marshmallow import fields

from src.api.schemas_config import JsonSchema

from pkg.json.validators import Range


class UploadSchema(JsonSchema):
	session = fields.Str(required=True)
	totalFileSize = fields.Int(required=True, validate=Range(min=1))
	totalChunkCount = fields.Int(required=True, validate=Range(min=1))
	chunkIndex = fields.Int(required=True, validate=Range(min=0))
	chunkByteOffset = fields.Int(required=True, validate=Range(min=0))


class ChunkSchema(JsonSchema):
	chunk = fields.Field(required=True)
