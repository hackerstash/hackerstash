from flask import Flask, session, g, redirect, request, url_for
from hackerstash.db import db
from hackerstash.models.user import User

from hackerstash.utils.assets import assets

from hackerstash.views.challenges import challenges
from hackerstash.views.contact import contact
from hackerstash.views.home import home
from hackerstash.views.leaderboard import leaderboard
from hackerstash.views.login import login
from hackerstash.views.past_results import past_results
from hackerstash.views.posts import posts
from hackerstash.views.profile import profile
from hackerstash.views.projects import projects
from hackerstash.views.rules import rules
from hackerstash.views.settings import settings
from hackerstash.views.signout import signout
from hackerstash.views.signup import signup
from hackerstash.views.users import users

app = Flask(__name__)
app.config.from_object('hackerstash.config.DevelopmentConfig')

app.register_blueprint(challenges)
app.register_blueprint(contact)
app.register_blueprint(home)
app.register_blueprint(leaderboard)
app.register_blueprint(login)
app.register_blueprint(past_results)
app.register_blueprint(posts)
app.register_blueprint(profile)
app.register_blueprint(projects)
app.register_blueprint(rules)
app.register_blueprint(settings)
app.register_blueprint(signout)
app.register_blueprint(signup)
app.register_blueprint(users)


@app.before_request
def before_request_func():
    if 'id' in session:
        g.user = User.query.get(session['id'])

        if not g.user.username and request.path != url_for('users.create'):
            return redirect(url_for('users.create'))


def create_app():
    db.init_app(app)
    assets.init_app(app)

    with app.app_context():
        db.create_all()

    return app
