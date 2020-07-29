from flask import Blueprint, render_template, request, session, redirect, url_for
from hackerstash.db import db
from hackerstash.models.user import User

users = Blueprint('users', __name__)


@users.route('/users/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('users/create.html')

    # TODO username exists

    user = User.query.get(session['id'])
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.username = request.form['username']
    db.session.commit()

    return redirect(url_for('users.show', user_id=user.id))


@users.route('/users/<user_id>')
def show(user_id):
    user = User.query.get(user_id)
    return render_template('users/show.html', user=user)
