from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_dance.contrib.google import google
from flask_dance.contrib.twitter import twitter
from hackerstash.db import db
from hackerstash.lib.invites import verify_invite
from hackerstash.models.user import User
from hackerstash.models.token import Token
from hackerstash.lib.emails.factory import email_factory

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        step = 1 if 'use_email' in request.args else 0
        return render_template('auth/login/index.html', step=step)

    email = request.form.get('email')
    code = request.form.get('code')

    user = User.query.filter_by(email=email).first()

    if not user:
        flash('An account with this email does not exist, please sign up')
        step = 1
    else:
        step = 2

        if code:
            valid = Token.verify(email, code)

            if valid:
                session['id'] = user.id
                Token.delete(email)
                return redirect(url_for('users.show', user_id=user.id))

            flash('The token is invalid')
        else:
            code = Token.generate(email)
            email_factory('login_token', email, {'token': code}).send()

    return render_template('auth/login/index.html', step=step, email=email)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        step = 1 if 'use_email' in request.args else 0
        return render_template('auth/signup/index.html', step=step)

    email = request.form.get('email')
    code = request.form.get('code')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('This email is in use, please log in')
        step = 1
    else:
        step = 2

        if code:
            valid = Token.verify(email, code)

            if valid:
                user = User(email=email)
                db.session.add(user)
                db.session.commit()
                session['id'] = user.id
                Token.delete(email)

                # If the user was invited but didn't have an
                # account, we can add them to the project now
                verify_invite(user)

                return redirect(url_for('users.show', user_id=user.id))

            flash('The token is invalid')
        else:
            code = Token.generate(email)
            email_factory('login_token', email, {'token': code}).send()

    return render_template('auth/signup/index.html', step=step, email=email)


@auth.route('/signout')
def signout():
    session.pop('id', None)
    return redirect(url_for('home.index'))


@auth.route('/login/google')
def google_login():
    return redirect(url_for('google.login'))


@auth.route('/login/twitter')
def twitter_login():
    return redirect(url_for('twitter.login'))


@auth.route('/login/google/callback')
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


@auth.route('/login/twitter/callback')
def twitter_callback():
    resp = twitter.get('account/verify_credentials.json?include_email=true')
    twitter_user = resp.json()

    user = User.query.filter_by(email=twitter_user['email']).first()

    if user:
        session['id'] = user.id
        return redirect(url_for('users.show', user_id=user.id))

    first_name, last_name = twitter_user['name'].split(' ')
    user = User(first_name=first_name, last_name=last_name, email=twitter_user['email'])
    db.session.add(user)
    db.session.commit()
    session['id'] = user.id

    # If the user was invited but didn't have an
    # account, we can add them to the project now
    verify_invite(user)

    return redirect(url_for('users.new'))
