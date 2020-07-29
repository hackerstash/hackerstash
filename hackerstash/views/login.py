from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from hackerstash.models.user import User

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
            # validate_token TODO
            session['id'] = user.id
            return redirect(url_for('users.show', user_id=user.id))

    return render_template('login/index.html', step=step, email=email)
