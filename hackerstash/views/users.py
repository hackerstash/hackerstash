import re
from flask import Blueprint, render_template, request, session, redirect, url_for, flash, g, jsonify
from sqlalchemy import or_
from hackerstash.db import db
from hackerstash.lib.images import upload_image, delete_image
from hackerstash.lib.invites import verify_invite
from hackerstash.lib.emails.factory import email_factory
from hackerstash.lib.logging import logging
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
        logging.info(f'{request.form["username"]} is already taken')
        flash('This username is already taken', 'failure')
        return render_template('users/new.html')

    user = User.query.get(session['id'])
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.username = re.sub(r'[^a-z0-9\_\-\.]+', '', request.form['username'], flags=re.IGNORECASE)
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
    logging.info(f'Deleteing user {g.user.username}')

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
    return redirect(url_for('users.show', user_id=user.id, saved=1))


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
        if key not in ['file', 'avatar', 'admin']:
            # Rich text always uses body as the key
            key = 'bio' if key == 'body' else key
            # Usernames must follow this pattern
            value = re.sub(r'[^a-z0-9\_\-\.]+', '', value, flags=re.IGNORECASE) if key == 'username' else value
            setattr(user, key, value)

    db.session.commit()
    return redirect(url_for('users.show', user_id=user.id, saved=1))


@users.route('/users/usernames')
@login_required
def get_usernames():
    query = request.args.get('q', '').lower()
    # You can search for users by their first name, last
    # name or by their username. A match in any of these
    # fields is good enough
    matching_users = User.query.filter(
        or_(
            User.username.ilike(f'%{query}%'),
            User.first_name.ilike(f'%{query}%'),
            User.last_name.ilike(f'%{query}%'),
        )
    ).limit(5).all()
    data = [{'name': f'{x.first_name} {x.last_name}', 'username': x.username} for x in matching_users]
    return jsonify(data)
