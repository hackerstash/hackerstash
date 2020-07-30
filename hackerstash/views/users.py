from flask import Blueprint, render_template, request, session, redirect, url_for, flash, g
from hackerstash.db import db
from hackerstash.lib.decorators import login_required
from hackerstash.models.user import User
from hackerstash.models.notification_setting import NotificationSetting

users = Blueprint('users', __name__)


@users.route('/users/<user_id>')
def show(user_id):
    user = User.query.get(user_id)
    return render_template('users/show.html', user=user)


@users.route('/users/new')
@login_required
def new():
    return render_template('users/new.html')


@users.route('/users/create', methods=['POST'])
@login_required
def create():
    if User.query.filter_by(username=request.form['username']).first():
        flash('This username is already taken')
        return render_template('users/new.html')

    user = User.query.get(session['id'])
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.username = request.form['username']
    user.notifications_settings = NotificationSetting()
    db.session.commit()

    return redirect(url_for('users.show', user_id=user.id))


@users.route('/users/destroy')
@login_required
def destroy():
    user = User.query.get(g.user.id)
    db.session.delete(user)
    db.session.commit()
    session.pop('id', None)

    return redirect(url_for('home.index'))
