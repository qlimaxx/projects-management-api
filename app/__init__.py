from flask import Flask

from .config import ProductionConfig


def create_app(config=ProductionConfig):
    app = Flask(__name__)
    app.config.from_object(config)

    from .models import db
    db.init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app
