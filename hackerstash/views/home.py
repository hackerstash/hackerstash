from flask import Blueprint, render_template, jsonify
from hackerstash.db import db
from hackerstash.lib.logging import logging
from hackerstash.lib.redis import redis

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
        logging.stack(e)
        return jsonify({'status': 'AHHHHHHHHH'}), 500
