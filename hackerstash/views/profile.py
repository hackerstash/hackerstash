from flask import Blueprint, render_template, redirect, url_for, g, request
from hackerstash.db import db
from hackerstash.lib.images import upload_image, delete_image
from hackerstash.models.user import User

profile = Blueprint('profile', __name__)


@profile.route('/profile')
def index():
    return render_template('profile/index.html')


@profile.route('/profile/update', methods=['POST'])
def update():
    user = User.query.get(g.user.id)

    if 'file' in request.files:
        key = upload_image(request.files['file'])
        user.avatar = key
    elif user.avatar:
        delete_image(user.avatar)
        user.avatar = None

    for key, value in request.form.items():
        if key != 'file':
            setattr(user, key, value)

    db.session.commit()
    return redirect(url_for('users.show', user_id=user.id))
