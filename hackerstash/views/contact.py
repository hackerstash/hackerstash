from flask import Blueprint, render_template, request, redirect, url_for
from hackerstash.config import config
from hackerstash.lib.emails.factory import email_factory
from hackerstash.lib.logging import Logging
from hackerstash.utils.recaptcha import recaptcha_required

log = Logging(module='Views::Contact')
contact = Blueprint('contact', __name__)


@contact.route('/contact', methods=['GET', 'POST'])
@recaptcha_required
def index() -> str:
    if request.method == 'GET':
        recaptcha_site_key = config['recaptcha_site_key']
        return render_template('contact/index.html', recaptcha_site_key=recaptcha_site_key, recaptcha=True)

    payload = {
        'name': request.form['name'],
        'email': request.form['email'],
        'subject': request.form['subject'],
        'message': request.form['message']
    }

    log.info('Sending contact email', {'payload': payload})
    email_factory('contact', 'hello@hackerstash.com', payload).send()
    return redirect(url_for('contact.index', success=True))
