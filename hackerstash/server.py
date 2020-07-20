from flask import Flask
from hackerstash.db import db

from hackerstash.views.home import home

app = Flask(__name__)
app.config.from_object('hackerstash.config.DevelopmentConfig')

app.register_blueprint(home)


def create_app():
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
