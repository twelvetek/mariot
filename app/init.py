from flask import Flask
from .config import Config
from .database import init_db, close_db
from .routes import main

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(main)

    app.teardown_appcontext(close_db)

    with app.app_context():
        init_db()

    return app