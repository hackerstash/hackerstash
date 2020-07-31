from flask import Blueprint, render_template, request
from hackerstash.lib.emails.factory import EmailFactory

contact = Blueprint('contact', __name__)


@contact.route('/contact', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('contact/index.html')

    # TODO recaptcha

    payload = {
        'name': request.form['name'],
        'email': request.form['email'],
        'subject': request.form['subject'],
        'message': request.form['message']
    }

    EmailFactory.create('CONTACT', payload).send()

    return render_template('contact/index.html')
