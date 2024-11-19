from flask import Flask

from app.api_routes import api_bp
from app.extensions import db, jwt, bcrypt, cors


def create_app():
    app = Flask(__name__)

    app.config.from_object('config.DevConfig')

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)

    app.register_blueprint(api_bp, url_prefix='/')

    with app.app_context():
        db.create_all()

    return app