from flask import Blueprint, render_template, g, request, redirect, url_for, flash
from hackerstash.models.transaction import Transaction  # TODO
from hackerstash.lib.logging import logging
from hackerstash.lib.emails.factory import email_factory
from hackerstash.utils.auth import login_required

stash = Blueprint('stash', __name__)


@stash.route('/stash', methods=['GET', 'POST'])
@login_required
def index() -> str:
    project = g.user.member.project

    if request.method == 'GET':
        return render_template('stash/index.html', project=project)

    stash_value = project.stash
    amount = request.form.get('value', type=int)
    message = request.form.get('message')

    logging.info(f'Receieved cash out request for \'{project.name}\'')

    if amount > stash_value:
        flash('There\'s not enough money in your Stash', 'failure')
    else:
        flash('Your Cash Out Request has been sent')
        payload = {'user': g.user, 'project': project, 'amount': amount, 'message': message}
        email_factory('cash_out_request', 'hello@hackerstash.com', payload).send()

    return redirect(url_for('stash.index'))
