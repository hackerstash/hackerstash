from flask import Blueprint, render_template

challenges = Blueprint('challenges', __name__)


@challenges.route('/challenges')
def index():
    return render_template('challenges/index.html')
