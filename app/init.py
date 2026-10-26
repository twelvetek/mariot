import logging

from flask import Flask
from app.routes import register_routes
from app.config import Config

def create_app():
    config = Config()
    config.log_file.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=str(config.log_file),
        level=config.log_level,
        format="%(asctime)s %(levelname)s %(message)s"
    )

    app = Flask(__name__)
    register_routes(app)

    return app