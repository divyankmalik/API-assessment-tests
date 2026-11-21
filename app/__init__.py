from flask import Flask, jsonify

from .errors import HttpError
from .routes.items import bp as items_bp


def create_app():
    app = Flask(__name__, static_folder="../static", static_url_path="")

    app.register_blueprint(items_bp)

    @app.get("/")
    def index():
        return app.send_static_file("index.html")

    @app.errorhandler(HttpError)
    def handle_http_error(err):
        status = getattr(err, "status", 500)
        
        
        return jsonify(error=err.message), status

    return app
