from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_dance.contrib.google import google
from hackerstash.db import db
from hackerstash.lib.invites import verify_invite
from hackerstash.models.user import User
from hackerstash.models.token import Tokens
from hackerstash.lib.emails.factory import EmailFactory

login = Blueprint('login', __name__)


@login.route('/login', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        step = 1 if 'use_email' in request.args else 0
        return render_template('login/index.html', step=step)

    email = request.form.get('email')
    code = request.form.get('code')

    user = User.query.filter_by(email=email).first()

    if not user:
        flash('An account with this email does not exist, please sign up')
        step = 1
    else:
        step = 2

        if code:
            valid = Tokens.verify(email, code)

            if valid:
                session['id'] = user.id
                Tokens.delete(email)
                return redirect(url_for('users.show', user_id=user.id))

            flash('The token is invalid')
        else:
            code = Tokens.generate(email)
            EmailFactory.create('LOGIN_TOKEN', email, {'token': code}).send()

    return render_template('login/index.html', step=step, email=email)


@login.route('/login/google')
def google_login():
    return redirect(url_for('google.login'))


@login.route('/login/google/callback')
def google_callback():
    resp = google.get('/oauth2/v1/userinfo')
    google_user = resp.json()

    user = User.query.filter_by(email=google_user['email']).first()

    if user:
        session['id'] = user.id
        return redirect(url_for('users.show', user_id=user.id))

    user = User(first_name=google_user['given_name'], last_name=google_user['family_name'], email=google_user['email'])
    db.session.add(user)
    db.session.commit()
    session['id'] = user.id

    # If the user was invited but didn't have an
    # account, we can add them to the project now
    verify_invite(user)

    return redirect(url_for('users.new'))
