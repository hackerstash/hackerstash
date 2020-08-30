from flask import Blueprint, render_template
from hackerstash.utils.auth import login_required

stash = Blueprint('stash', __name__)


@stash.route('/stash')
@login_required
def index() -> str:
    return render_template('stash/index.html')
