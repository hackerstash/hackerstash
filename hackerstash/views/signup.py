from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from hackerstash.db import db
from hackerstash.models.user import User
from hackerstash.models.token import Tokens
from hackerstash.lib.emails.factory import EmailFactory

# TODO remove when in use
from hackerstash.models.notification import Notification

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
            valid = Tokens.verify(email, code)

            if valid:
                user = User(email=email)
                db.session.add(user)
                db.session.commit()
                session['id'] = user.id
                Tokens.delete(email)
                return redirect(url_for('users.show', user_id=user.id))

            flash('The token is invalid')
        else:
            code = Tokens.generate(email)
            EmailFactory.create('LOGIN_TOKEN', email, {'token': code}).send()

    return render_template('signup/index.html', step=step, email=email)
