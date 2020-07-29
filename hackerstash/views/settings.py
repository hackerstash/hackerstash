from flask import Blueprint, render_template, redirect, url_for, g, request
from hackerstash.db import db
from hackerstash.lib.decorators import login_required
from hackerstash.models.user import User

settings = Blueprint('settings', __name__)


@settings.route('/settings')
@login_required
def index():
    return render_template('settings/index.html')


@settings.route('/settings/update', methods=['POST'])
@login_required
def update():
    user = User.query.get(g.user.id)
    user.email = request.form['email']
    user.telephone = request.form['telephone']
    db.session.commit()
    return redirect(url_for('users.show', user_id=user.id))


@settings.route('/settings/destroy')
@login_required
def destroy():
    return redirect(url_for('home.index'))
