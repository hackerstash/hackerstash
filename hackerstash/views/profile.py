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

    # Flask adds the empty file for some reason
    if 'file' in request.files and request.files['file'].filename != '':
        key = upload_image(request.files['file'])
        user.avatar = key
    elif not request.form['avatar'] and user.avatar:
        delete_image(user.avatar)
        user.avatar = None

    for key, value in request.form.items():
        if key not in ['file', 'avatar']:
            setattr(user, key, value)

    db.session.commit()
    return redirect(url_for('users.show', user_id=user.id))
