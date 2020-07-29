from flask import Flask
from hackerstash.db import db

from hackerstash.utils.assets import assets

from hackerstash.views.contact import contact
from hackerstash.views.home import home
from hackerstash.views.leaderboard import leaderboard
from hackerstash.views.past_results import past_results
from hackerstash.views.posts import posts
from hackerstash.views.projects import projects
from hackerstash.views.rules import rules

app = Flask(__name__)
app.config.from_object('hackerstash.config.DevelopmentConfig')

app.register_blueprint(contact)
app.register_blueprint(home)
app.register_blueprint(leaderboard)
app.register_blueprint(past_results)
app.register_blueprint(posts)
app.register_blueprint(projects)
app.register_blueprint(rules)


def create_app():
    db.init_app(app)
    assets.init_app(app)

    with app.app_context():
        db.create_all()

    return app
