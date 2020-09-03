from flask import Blueprint, render_template, g
from hackerstash.models.transaction import Transaction  # TODO
from hackerstash.utils.auth import login_required

stash = Blueprint('stash', __name__)


@stash.route('/stash')
@login_required
def index() -> str:
    project = g.user.member.project
    return render_template('stash/index.html', project=project)
