
import logging 
from flask import render_template


def register_routes(app):

    @app.route("/")
    def index():
        logging.info("Rendering index page")
        return render_template("index.html")