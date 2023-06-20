
from flask import Flask
# from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import redis

# Globally accessible libraries
db = SQLAlchemy()
r = FlaskRedis()
# login_manager = LoginManager()
migrate = Migrate()
ma = Marshmallow()
cors = CORS()


def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('apps.config.Config')
    cache = redis.Redis(host='redis', port=6379)

    # Initialize Plugins
    initialize_extensions(app)

    # Register Blueprints
    with app.app_context():
        register_blueprints(app)

    return app


### Helper Functions ###
def register_blueprints(app):
    from apps.home import home_bp
    from apps.authentication import auth_bp
    from apps.ai_text import aitext_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(aitext_bp)


def initialize_extensions(app):
    db.init_app(app)
    # login_manager.create_app(app)
    r.init_app(app)


def register_error_handlers(app):
    pass


def configure_logging(app):
    pass
