from flask import Blueprint, render_template, request, redirect, url_for, make_response
from hackerstash.models.waitlist import Waitlist

home = Blueprint('home', __name__)


@home.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        waitlist_count = Waitlist.query.count()
        added_to_waitlist = request.cookies.get('added_to_waitlist')

        return render_template(
            'home/index.html',
            waitlist_count=waitlist_count,
            added_to_waitlist=added_to_waitlist
        )

    Waitlist.create_is_not_exists(first_name=request.form['first_name'], email=request.form['email'])
    resp = make_response(redirect(url_for('home.index')))
    resp.set_cookie('added_to_waitlist', '1', max_age=31557600)

    return resp
