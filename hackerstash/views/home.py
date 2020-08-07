from flask import Blueprint, render_template, request, redirect, url_for, make_response
from hackerstash.config import config
from hackerstash.models.waitlist import Waitlist
from hackerstash.lib.emails.factory import email_factory
from hackerstash.utils.recaptcha import recaptcha_required

home = Blueprint('home', __name__)


@home.route('/', methods=['GET', 'POST'])
@recaptcha_required
def index():
    if request.method == 'GET':
        waitlist_count = Waitlist.query.count()
        added_to_waitlist = request.cookies.get('added_to_waitlist')
        recaptcha_site_key = config['recaptcha_site_key']

        return render_template(
            'home/index.html',
            waitlist_count=waitlist_count,
            added_to_waitlist=added_to_waitlist,
            recaptcha_site_key=recaptcha_site_key
        )

    first_mame = request.form['first_name']
    email = request.form['email']

    Waitlist.create_is_not_exists(first_name=first_mame, email=email)
    email_factory('waitlist_confirmation', email, {'first_name': first_mame, 'email': email}).send()

    resp = make_response(redirect(url_for('home.index')))
    resp.set_cookie('added_to_waitlist', '1', max_age=31557600)

    return resp
