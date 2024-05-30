from urllib.parse import urlparse
from redis import Redis

from src.app import app


url = urlparse(app.config['REDIS_CONN_URL'])
redis = Redis(
	host = url.hostname,
	port = url.port,
	password = url.password,
	decode_responses = True
)