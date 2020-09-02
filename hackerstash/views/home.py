from flask import Blueprint, render_template, request, redirect, url_for, make_response, jsonify
from hackerstash.db import db
from hackerstash.config import config
from hackerstash.models.waitlist import Waitlist
from hackerstash.lib.emails.factory import email_factory
from hackerstash.lib.logging import logging
from hackerstash.lib.redis import redis
from hackerstash.utils.recaptcha import recaptcha_required

home = Blueprint('home', __name__)


@home.route('/', methods=['GET', 'POST'])
@recaptcha_required
def index() -> str:
    if request.method == 'GET':
        params = {
            'waitlist_count': Waitlist.query.count(),
            'added_to_waitlist': request.cookies.get('added_to_waitlist'),
            'recaptcha_site_key': config['recaptcha_site_key']
        }
        return render_template('home/index.html', **params)

    first_mame = request.form['first_name']
    email = request.form['email']

    logging.info(f'Adding {first_mame} ({email}) to the waitlist')
    Waitlist.create_is_not_exists(first_name=first_mame, email=email)
    email_factory('waitlist_confirmation', email, {'first_name': first_mame, 'email': email}).send()

    resp = make_response(redirect(url_for('home.index')))
    resp.set_cookie('added_to_waitlist', '1', max_age=31557600)
    return resp


@home.route('/__ping')
def ping():
    try:
        db.engine.execute('SELECT 1')
        redis.keys('*')
        return jsonify({'status': 'PONG! Have a nice day.'})
    except Exception as e:
        logging.stack(e)
        return jsonify({'status': 'AHHHHHHHHH'}), 500
