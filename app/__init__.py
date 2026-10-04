from pathlib import Path

from flask import Flask, session

from config import Config
from . import database


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)

    database.init_app(app)

    from .blueprints.auth import bp as auth_bp
    from .blueprints.learning import bp as learning_bp
    from .blueprints.main import bp as main_bp
    from .blueprints.profile import bp as profile_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(learning_bp, url_prefix="/aprender")
    app.register_blueprint(profile_bp, url_prefix="/perfil")

    @app.context_processor
    def inject_globals():
        return {"csrf_token": session.get("csrf_token", "")}

    @app.after_request
    def security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), geolocation=(), microphone=(self)"
        return response

    with app.app_context():
        database.init_db()

    return app
