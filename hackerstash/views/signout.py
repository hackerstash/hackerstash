from flask import Blueprint, redirect, url_for, session

signout = Blueprint('signout', __name__)


@signout.route('/signout')
def index():
    session.pop('id', None)
    return redirect(url_for('home.index'))
