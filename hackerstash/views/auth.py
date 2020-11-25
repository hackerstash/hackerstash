from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_dance.contrib.google import google
from flask_dance.contrib.twitter import twitter
from hackerstash.db import db
from hackerstash.lib.images import Images
from hackerstash.lib.logging import Logging
from hackerstash.lib.tokens import Tokens
from hackerstash.models.user import User
from hackerstash.lib.emails.factory import email_factory

log = Logging(module='Views::Auth')
auth = Blueprint('auth', __name__)


def set_session(user):
    session['id'] = user.id
    session.permanent = True


@auth.route('/login', methods=['GET', 'POST'])
def login() -> str:
    """
    Render the login page
    :return: str
    """
    if request.method == 'GET':
        step = 1 if 'use_email' in request.args else 0
        return render_template('auth/login.html', step=step)

    email = request.form.get('email')
    code = request.form.get('code')
    user = User.query.filter_by(email=email).first()

    if not user:
        flash('An account with this email does not exist, please sign up', 'failure')
        step = 1
    else:
        step = 2

        if code:
            if Tokens.verify(email, code):
                set_session(user)
                Tokens.delete(email)
                return redirect(url_for('users.show', user_id=user.id))

            log.warn('Incorrect code submitted', {'email': email, 'code': code})
            flash('The token is invalid', 'failure')
        else:
            code = Tokens.generate(email)
            email_factory('login_token', email, {'token': code}).send()

    return render_template('auth/login.html', step=step, email=email)


@auth.route('/signup', methods=['GET', 'POST'])
def signup() -> str:
    """
    Render the sign up page
    :return: str
    """
    if request.method == 'GET':
        step = 1 if 'use_email' in request.args else 0
        return render_template('auth/signup.html', step=step)

    email = request.form['email']
    code = request.form.get('code')
    user = User.query.filter_by(email=email).first()

    if user:
        flash('This email is in use, please log in', 'failure')
        step = 1
    else:
        step = 2

        if code:
            if Tokens.verify(email, code):
                user = User(email=email)
                db.session.add(user)
                db.session.commit()
                set_session(user)
                Tokens.delete(email)
                return redirect(url_for('users.show', user_id=user.id))

            log.warn('Incorrect code submitted', {'email': email, 'code': code})
            flash('The token is invalid', 'failure')
        else:
            code = Tokens.generate(email)
            email_factory('login_token', email, {'token': code}).send()

    return render_template('auth/signup.html', step=step, email=email)


@auth.route('/signout')
def signout() -> str:
    """
    Sign the user and redirect to the home page
    :return: str
    """
    session.pop('id', None)
    return redirect(url_for('home.index'))


@auth.route('/login/google')
def google_login() -> str:
    """
    Redirect to the google login page
    :return: str
    """
    return redirect(url_for('google.login'))


@auth.route('/login/twitter')
def twitter_login() -> str:
    """
    Redirect to the twitter login page
    :return: str
    """
    return redirect(url_for('twitter.login'))


@auth.route('/login/google/callback')
def google_callback() -> str:
    """
    Handle the google callback
    :return: str
    """
    resp = google.get('/oauth2/v1/userinfo')
    google_user = resp.json()

    if not google_user.get('email'):
        log.warn('Google user payload did not contain an email', {'google_user': google_user})
        flash('Google could not provide us with a complete profile, please pick a different auth type', 'failure')
        return redirect(url_for('auth.signup'))

    user = User.query.filter_by(email=google_user['email']).first()

    if user:
        set_session(user)
        return redirect(url_for('users.show', user_id=user.id))

    # Use their google photo if it exists
    key = Images.upload_from_url(google_user['picture']) if google_user['picture'] else None

    user = User(
        first_name=google_user.get('given_name'),
        last_name=google_user.get('family_name'),
        email=google_user['email'],
        avatar=key
    )
    db.session.add(user)
    db.session.commit()
    set_session(user)

    return redirect(url_for('onboarding.index'))


@auth.route('/login/twitter/callback')
def twitter_callback() -> str:
    """
    Handle the twitter callback
    :return: str
    """
    resp = twitter.get('account/verify_credentials.json?include_email=true')
    twitter_user = resp.json()

    if not twitter_user.get('email'):
        log.warn('Twitter user payload did not contain an email', {'twitter_user': twitter_user})
        flash('Twitter could not provide us with a complete profile, please pick a different auth type', 'failure')
        return redirect(url_for('auth.signup'))

    user = User.query.filter_by(email=twitter_user['email']).first()

    if user:
        set_session(user)
        return redirect(url_for('users.show', user_id=user.id))

    name = twitter_user['name'].split(' ')
    # Some people only have their first name on twitter which
    # causes and index out of bounds error
    if len(name) == 2:
        first_name = name[0]
        last_name = name[1]
    else:
        first_name = name[0]
        last_name = None

    # Use their twitter photo if it exists
    key = Images.upload_from_url(twitter_user['profile_image_url']) if twitter_user['profile_image_url'] else None

    user = User(
        first_name=first_name,
        last_name=last_name,
        email=twitter_user['email'],
        avatar=key
    )
    db.session.add(user)
    db.session.commit()
    set_session(user)

    return redirect(url_for('onboarding.index'))
