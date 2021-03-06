from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


login_manager = LoginManager()
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')

    register_buleprint(app)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "web.login"
    login_manager.login_message = "请先登录或注册"
    with app.app_context():
        db.create_all()

    return app


def register_buleprint(app):
    from app.web.book import web
    app.register_blueprint(web)
