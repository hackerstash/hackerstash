from flask import Blueprint, render_template, jsonify
from hackerstash.db import db
from hackerstash.lib.logging import Logging
from hackerstash.lib.redis import redis

log = Logging(module='Views::Home')
home = Blueprint('home', __name__)


@home.route('/', methods=['GET', 'POST'])
def index() -> str:
    return render_template('home/index.html')


@home.route('/__ping')
def ping():
    try:
        db.engine.execute('SELECT 1')
        redis.keys('*')
        return jsonify({'status': 'PONG! Have a nice day.'})
    except Exception as e:
        log.error('Failed to ping!', e)
        return jsonify({'status': 'AHHHHHHHHH'}), 500
