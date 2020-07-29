from flask import Blueprint, render_template, redirect, url_for, g, request
from hackerstash.db import db
from hackerstash.models.user import User

profile = Blueprint('profile', __name__)


@profile.route('/settings')
def index():
    return render_template('profile/index.html')


@profile.route('/settings/update', methods=['POST'])
def update():
    user = User.query.get(g.user.id)

    print(request.files)

    for key, value in request.form.items():
        if key != 'file':
            setattr(user, key, value)

    db.session.commit()
    return redirect(url_for('users.show', user_id=user.id))
