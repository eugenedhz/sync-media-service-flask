from flask import Flask


def create_app():
    app = Flask(__name__)

    return app


# Create Flask application
app = create_app()