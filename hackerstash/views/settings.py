from flask import Blueprint, render_template, redirect, url_for, g, request
from hackerstash.db import db
from hackerstash.models.user import User

settings = Blueprint('settings', __name__)


@settings.route('/settings')
def index():
    return render_template('settings/index.html')


@settings.route('/settings/update', methods=['POST'])
def update():
    user = User.query.get(g.user.id)
    user.email = request.form['email']
    user.telephone = request.form['telephone']
    db.session.commit()
    return redirect(url_for('users.show', user_id=user.id))


@settings.route('/settings/destroy')
def destroy():
    return redirect(url_for('home.index'))
