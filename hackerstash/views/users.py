from flask import Blueprint, render_template, request, session, redirect, url_for, flash, g
from hackerstash.db import db
from hackerstash.lib.images import upload_image, delete_image
from hackerstash.lib.invites import verify_invite
from hackerstash.lib.emails.factory import email_factory
from hackerstash.lib.notifications.factory import notification_factory
from hackerstash.models.user import User
from hackerstash.models.notification_setting import NotificationSetting
from hackerstash.utils.auth import login_required

users = Blueprint('users', __name__)


@users.route('/users/<user_id>')
def show(user_id: str) -> str:
    user = User.query.get(user_id)
    if not user:
        return render_template('users/404.html')
    return render_template('users/show.html', user=user)


@users.route('/users/<user_id>/followers')
def followers(user_id: str) -> str:
    user = User.query.get(user_id)
    return render_template('users/followers/index.html', user=user)


@users.route('/users/<user_id>/following')
def following(user_id: str) -> str:
    user = User.query.get(user_id)
    return render_template('users/following/index.html', user=user)


@users.route('/users/new')
@login_required
def new() -> str:
    return render_template('users/new.html')


@users.route('/users/<user_id>/follow')
@login_required
def follow(user_id: str) -> str:
    user = User.query.get(user_id)
    if g.user.is_following(user):
        g.user.unfollow(user)
    else:
        g.user.follow(user)
        notification_factory('follower_created', {'user': user, 'follower': g.user}).publish()
    db.session.commit()
    return redirect(url_for('users.show', user_id=user.id))


@users.route('/users/create', methods=['POST'])
@login_required
def create() -> str:
    if User.query.filter_by(username=request.form['username']).first():
        flash('This username is already taken', 'failure')
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

    # If the user was invited but didn't have an
    # account, we can add them to the project now
    verify_invite(user)

    return redirect(url_for('users.show', user_id=user.id))


@users.route('/users/destroy')
@login_required
def destroy() -> str:
    user = User.query.get(g.user.id)

    # Can't think of a way to cascade this at the db level
    if user.member and len(user.member.project.members) == 1:
        db.session.delete(user.member.project)

    email_factory('close_account', user.email, {}).send()

    db.session.delete(user)
    db.session.commit()
    session.pop('id', None)

    return redirect(url_for('home.index'))


@users.route('/users/settings')
@login_required
def edit_settings() -> str:
    return render_template('users/settings/edit.html')


@users.route('/users/settings/update', methods=['POST'])
@login_required
def update_settings() -> str:
    user = User.query.get(g.user.id)
    user.email = request.form['email']
    user.telephone = request.form['telephone']
    db.session.commit()
    flash('Your setting have been updated', 'success')
    return redirect(url_for('users.show', user_id=user.id))


@users.route('/users/profile')
def edit_profile() -> str:
    return render_template('users/profile/edit.html')


@users.route('/users/profile/update', methods=['POST'])
def update_profile() -> str:
    user = User.query.get(g.user.id)

    # Flask adds the empty file for some reason
    if 'file' in request.files and request.files['file'].filename != '':
        key = upload_image(request.files['file'])
        user.avatar = key
    elif not request.form['avatar'] and user.avatar:
        delete_image(user.avatar)
        user.avatar = None

    for key, value in request.form.items():
        if key not in ['file', 'avatar']:
            setattr(user, key, value)

    db.session.commit()
    flash('Your setting have been updated', 'success')
    return redirect(url_for('users.show', user_id=user.id))
