from flask import Flask
from hackerstash.config import config
from hackerstash.db import db

from hackerstash.utils.assets import assets
from hackerstash.utils import filters
from hackerstash.utils import hooks

from hackerstash.views.api.admin import api_admin
from hackerstash.views.api.locations import api_locations

from hackerstash.views.auth import auth
from hackerstash.views.challenges import challenges
from hackerstash.views.contact import contact
from hackerstash.views.developers import developers
from hackerstash.views.home import home
from hackerstash.views.leaderboard import leaderboard
from hackerstash.views.legal import legal
from hackerstash.views.notifications import notifications
from hackerstash.views.past_results import past_results
from hackerstash.views.posts import posts
from hackerstash.views.projects import projects
from hackerstash.views.rules import rules
from hackerstash.views.users import users

from hackerstash.lib.oauth import google_blueprint, twitter_blueprint

app = Flask(__name__)

app.debug = config['debug']
app.secret_key = config['secret']
app.config['SQLALCHEMY_DATABASE_URI'] = config['sqlalchemy_database_uri']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config['sqlalchemy_track_notifications']

# Add API blueprints
app.register_blueprint(api_admin)
app.register_blueprint(api_locations)

# Add regular blueprints
app.register_blueprint(auth)
app.register_blueprint(challenges)
app.register_blueprint(contact)
app.register_blueprint(developers)
app.register_blueprint(home)
app.register_blueprint(leaderboard)
app.register_blueprint(legal)
app.register_blueprint(notifications)
app.register_blueprint(past_results)
app.register_blueprint(posts)
app.register_blueprint(projects)
app.register_blueprint(rules)
app.register_blueprint(users)

# Add blueprints for flask_dance
app.register_blueprint(google_blueprint)
app.register_blueprint(twitter_blueprint)


def create_app():
    db.init_app(app)
    assets.init_app(app)
    filters.init_app(app)
    hooks.init_app(app)

    # with app.app_context():
    #     db.create_all()

    return app
