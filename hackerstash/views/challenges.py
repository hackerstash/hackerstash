from flask import Blueprint, render_template
from hackerstash.lib.decorators import login_required

challenges = Blueprint('challenges', __name__)


@challenges.route('/challenges')
@login_required
def index():
    return render_template('challenges/index.html')
