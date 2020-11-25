import requests
from functools import wraps
from flask import request
from werkzeug.exceptions import Forbidden
from hackerstash.config import config
from hackerstash.lib.logging import Logging

log = Logging(module='Recaptcha')


def recaptcha_required(f):
    """
    A decorator that checks if the incoming form submitter
    can be trusted
    :param f: function
    :return: function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method != 'GET':
            token = request.form.get('g-recaptcha-response')

            if not token:
                log.warn('No recaptcha token submitted')
                raise Forbidden()

            data = {
                'secret': config['recaptcha_secret_key'],
                'response': token
            }

            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            r = requests.post('https://www.google.com/recaptcha/api/siteverify', headers=headers, data=data)
            r.raise_for_status()
            response = r.json()

            if not response['success'] or response['score'] < 0.7:
                log.warn('Recaptcha failed', {'response': response})
                raise Forbidden()

        return f(*args, **kwargs)
    return decorated_function
