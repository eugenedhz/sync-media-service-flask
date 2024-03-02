from flask import Flask

from src.api.extensions import jwt, cors, socketio, swagger
from src.configs.app_config import Development


def create_app() -> Flask:
    app = Flask(__name__)
    
    app.config.from_object(Development())

    socketio.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    swagger.init_app(app)

    return app


app = create_app()