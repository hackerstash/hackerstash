from flask import Blueprint, render_template, request, session, redirect, url_for, flash, g
from hackerstash.db import db
from hackerstash.lib.images import upload_image
from hackerstash.lib.notifications.factory import NotificationFactory
from hackerstash.models.user import User
from hackerstash.models.notification_setting import NotificationSetting
from hackerstash.utils.auth import login_required

users = Blueprint('users', __name__)


@users.route('/users/<user_id>')
def show(user_id):
    user = User.query.get(user_id)

    if not user:
        return render_template('users/404.html')

    return render_template('users/show.html', user=user)


@users.route('/users/<user_id>/followers')
def followers(user_id):
    user = User.query.get(user_id)
    return render_template('users/followers/index.html', user=user)


@users.route('/users/<user_id>/following')
def following(user_id):
    user = User.query.get(user_id)
    return render_template('users/following/index.html', user=user)


@users.route('/users/new')
@login_required
def new():
    return render_template('users/new.html')


@users.route('/users/<user_id>/follow')
@login_required
def follow(user_id):
    user = User.query.get(user_id)
    if g.user.is_following(user):
        g.user.unfollow(user)
    else:
        g.user.follow(user)
        NotificationFactory.create('FOLLOWER_CREATED', {'user': user, 'follower': g.user}).publish()
    db.session.commit()
    return redirect(url_for('users.show', user_id=user.id))


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

    # Flask adds the empty file for some reason
    if 'file' in request.files and request.files['file'].filename != '':
        key = upload_image(request.files['file'])
        user.avatar = key

    db.session.commit()

    return redirect(url_for('users.show', user_id=user.id))


@users.route('/users/destroy')
@login_required
def destroy():
    user = User.query.get(g.user.id)

    # Can't think of a way to cascade this at the db level
    if user.member and len(user.member.project.members) == 1:
        db.session.delete(user.member.project)

    db.session.delete(user)
    db.session.commit()
    session.pop('id', None)

    return redirect(url_for('home.index'))
