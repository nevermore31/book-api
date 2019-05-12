# from werkzeug.contrib.fixers import ProxyFix
from flask import Flask
from .setting import Config
from .ext import db, cors, loginmanaer
from .url import kanman_api


def create_app(config=Config):
    app = Flask(__name__)
    # app.wsgi_app = ProxyFix(app.wsgi_app)
    app.config.from_object(config)
    app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))

    db.init_app(app)

    db.create_all(app=app)

    cors.init_app(app)
    loginmanaer.init_app(app)

    kanman_api.init_app(app)

    return app