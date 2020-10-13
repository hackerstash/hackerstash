from flask import Blueprint, render_template, g, request, redirect, url_for, flash
from hackerstash.models.transaction import Transaction  # TODO
from hackerstash.lib.logging import Logging
from hackerstash.lib.emails.factory import email_factory
from hackerstash.utils.auth import login_required

log = Logging(module='Views::Stash')
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

    log.info('Receieved cash out request', {'project_id': project.id, 'payload': request.form})

    if amount > stash_value:
        log.info('Not enough funds', {'project_id': project.id})
        flash('There\'s not enough money in your Stash', 'failure')
    else:
        flash('Your Cash Out Request has been sent')
        payload = {'user': g.user, 'project': project, 'amount': amount, 'message': message}
        email_factory('cash_out_request', 'hello@hackerstash.com', payload).send()

    return redirect(url_for('stash.index'))
