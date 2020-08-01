from flask import Flask, session, g, redirect, request, url_for, render_template
from hackerstash.config import config
from hackerstash.db import db
from hackerstash.models.user import User

from hackerstash.utils.assets import assets
from hackerstash.utils import filters
from hackerstash.utils.sidebar import sidebar_data

from hackerstash.views.challenges import challenges
from hackerstash.views.contact import contact
from hackerstash.views.home import home
from hackerstash.views.leaderboard import leaderboard
from hackerstash.views.login import login
from hackerstash.views.notifications import notifications
from hackerstash.views.past_results import past_results
from hackerstash.views.posts import posts
from hackerstash.views.profile import profile
from hackerstash.views.projects import projects
from hackerstash.views.rules import rules
from hackerstash.views.settings import settings
from hackerstash.views.signout import signout
from hackerstash.views.signup import signup
from hackerstash.views.users import users

from hackerstash.lib.oauth import google_blueprint, twitter_blueprint

app = Flask(__name__)

app.debug = config['debug']
app.secret_key = config['secret']
app.config['SQLALCHEMY_DATABASE_URI'] = config['sqlalchemy_database_uri']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config['sqlalchemy_track_notifications']

app.register_blueprint(challenges)
app.register_blueprint(contact)
app.register_blueprint(home)
app.register_blueprint(leaderboard)
app.register_blueprint(login)
app.register_blueprint(notifications)
app.register_blueprint(past_results)
app.register_blueprint(posts)
app.register_blueprint(profile)
app.register_blueprint(projects)
app.register_blueprint(rules)
app.register_blueprint(settings)
app.register_blueprint(signout)
app.register_blueprint(signup)
app.register_blueprint(users)

app.register_blueprint(google_blueprint)
app.register_blueprint(twitter_blueprint)


@app.before_request
def before_request_func():
    if 'id' in session:
        g.user = User.query.get(session['id'])

        if not g.user.username and request.path not in [url_for('users.new'), url_for('users.create')]:
            return redirect(url_for('users.new'))

    prize_pool, time_remaining = sidebar_data()
    g.prize_pool = prize_pool
    g.time_remaining = time_remaining


@app.errorhandler(404)
def page_not_found(_error):
    return render_template('404.html'), 404


def create_app():
    db.init_app(app)
    assets.init_app(app)
    filters.init_app(app)

    with app.app_context():
        db.create_all()

    return app
