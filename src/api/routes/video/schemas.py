from marshmallow import fields

from src.api.schemas_config import JsonSchema


class UploadSchema(JsonSchema):
	session = fields.Str(required=True)
	totalFileSize = fields.Int(required=True)
	totalChunkCount = fields.Int(required=True)
	chunkIndex = fields.Int(required=True)
	chunkByteOffset = fields.Int(required=True)


class ChunkSchema(JsonSchema):
	chunk = fields.Field(required=True)
