from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from hackerstash.db import db
from hackerstash.models.user import User

# TODO remove when in use
from hackerstash.models.member import Member
from hackerstash.models.project import Project
from hackerstash.models.comment import Comment
from hackerstash.models.post import Post
from hackerstash.models.notification import Notification
from hackerstash.models.notification_setting import NotificationSetting
from hackerstash.models.invite import Invite

signup = Blueprint('signup', __name__)


@signup.route('/signup', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        step = 1 if 'use_email' in request.args else 0
        return render_template('signup/index.html', step=step)

    email = request.form.get('email')
    code = request.form.get('code')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('This email is in use, please log in')
        step = 1
    else:
        step = 2

        if code:
            # validate_token TODO
            user = User(email=email)
            db.session.add(user)
            db.session.commit()
            session['id'] = user.id
            return redirect(url_for('users.show', user_id=user.id))

    return render_template('signup/index.html', step=step, email=email)
