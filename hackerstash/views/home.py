from flask import Blueprint, render_template, jsonify, redirect, url_for
from hackerstash.db import db
from hackerstash.lib.logging import Logging
from hackerstash.lib.redis import redis

log = Logging(module='Views::Home')
home = Blueprint('home', __name__)


@home.route('/')
def index() -> str:
    """
    Render the home page
    :return: str
    """
    return render_template('home/index.html')


@home.route('/favicon.ico')
def favicon():
    """
    Not sure where else to put this, but Chrome insists
    # on requesting it from here regardless of what I put
    # in the <head> tag
    :return: Response
    """
    return redirect(url_for('static', filename='images/favicon.ico'))


@home.route('/__ping')
def ping():
    """
    Test that the app can talk to redis and the database
    :return: str
    """
    try:
        db.engine.execute('SELECT 1')
        redis.keys('*')
        return jsonify({'status': 'PONG! Have a nice day.'})
    except Exception as e:
        log.error('Failed to ping!', e)
        return jsonify({'status': 'AHHHHHHHHH'}), 500
