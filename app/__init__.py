from flask import Flask

from app.models.base import db
from app.web.book import web


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_buleprint(app)
    db.init_app(app)
    db.create_all(app=app)
    with app.app_context():
        db.create_all()
    return app


def register_buleprint(app):
    app.register_blueprint(web)
    from app.models.book import Book
    from app.models.user import User
    from app.models.gift import Gift
