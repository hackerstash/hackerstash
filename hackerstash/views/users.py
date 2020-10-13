import re
from flask import Blueprint, render_template, request, session, redirect, url_for, flash, g, jsonify
from sqlalchemy import or_
from hackerstash.db import db
from hackerstash.lib.images import Images
from hackerstash.lib.invites import Invites
from hackerstash.lib.emails.factory import email_factory
from hackerstash.lib.logging import Logging
from hackerstash.lib.notifications.factory import notification_factory
from hackerstash.models.user import User
from hackerstash.models.notification_setting import NotificationSetting
from hackerstash.utils.auth import login_required
from hackerstash.utils.helpers import get_html_text_length

log = Logging(module='Views::Users')
users = Blueprint('users', __name__)


@users.route('/users/<user_id>')
def show(user_id: str) -> str:
    if user_id.isnumeric():
        user = User.query.get(user_id)
    else:
        user = User.query.filter_by(username=user_id).first()
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
        log.info('Unfollowing user', {'user_id': g.user.id, 'follow_id': user.id})
        g.user.unfollow(user)
    else:
        log.info('Following user', {'user_id': g.user.id, 'follow_id': user.id})
        g.user.follow(user)
        notification_factory('follower_created', {'user': user, 'follower': g.user}).publish()
    db.session.commit()
    return redirect(url_for('users.show', user_id=user.id))


@users.route('/users/create', methods=['POST'])
@login_required
def create() -> str:
    log.info('Creating user', {'user_data': request.form})
    if User.query.filter_by(username=request.form['username']).first():
        log.warn('Username is already taken', {'username': request.form['username']})
        flash('This username is already taken', 'failure')
        return render_template('users/new.html')

    user = User.query.get(session['id'])
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.username = re.sub(r'[^a-z0-9\_\-\.]+', '', request.form['username'], flags=re.IGNORECASE)
    user.notifications_settings = NotificationSetting()

    # Flask adds the empty file for some reason
    if 'file' in request.files and request.files['file'].filename != '':
        key = Images.upload(request.files['file'])
        user.avatar = key

    db.session.commit()

    # If the user was invited but didn't have an
    # account, we can add them to the project now
    Invites.verify(user)

    return redirect(url_for('users.show', user_id=user.id))


@users.route('/users/destroy')
@login_required
def destroy() -> str:
    log.info('Deleteing user', {'user_id': g.user.id})

    # Can't think of a way to cascade this at the db level
    if g.user.member and len(g.user.member.project.members) == 1:
        db.session.delete(g.user.member.project)

    email_factory('close_account', g.user.email, {}).send()

    db.session.delete(g.user)
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
    log.info('Updating user settings', {'user_id': g.user.id, 'user_data': request.form})
    g.user.email = request.form['email']
    g.user.telephone = request.form['telephone']
    db.session.commit()
    return redirect(url_for('users.show', user_id=g.user.id, saved=1))


@users.route('/users/profile')
@login_required
def edit_profile() -> str:
    return render_template('users/profile/edit.html')


@users.route('/users/profile/update', methods=['POST'])
@login_required
def update_profile() -> str:
    log.info('Updating user profile', {'user_id': g.user.id, 'user_data': request.form})

    if get_html_text_length(request.form['body']) > 240:
        flash('User bio exceeds 240 characters', 'failure')
        return redirect(url_for('users.edit_profile'))

    # Flask adds the empty file for some reason
    if 'file' in request.files and request.files['file'].filename != '':
        key = Images.upload(request.files['file'])
        g.user.avatar = key
    elif not request.form['avatar'] and g.user.avatar:
        Images.delete(g.user.avatar)
        g.user.avatar = None

    for key, value in request.form.items():
        if key not in ['file', 'avatar', 'admin']:
            # Rich text always uses body as the key
            key = 'bio' if key == 'body' else key
            # Usernames must follow this pattern
            value = re.sub(r'[^a-z0-9\_\-\.]+', '', value, flags=re.IGNORECASE) if key == 'username' else value
            setattr(g.user, key, value)

    db.session.commit()
    return redirect(url_for('users.show', user_id=g.user.id, saved=1))


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
