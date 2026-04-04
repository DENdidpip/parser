from flask import Flask
from .config import Config
from .user import db
from .routes import main_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    app.register_blueprint(main_bp)

    return app