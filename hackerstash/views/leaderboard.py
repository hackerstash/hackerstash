from flask import Blueprint, render_template

leaderboard = Blueprint('leaderboard', __name__)


@leaderboard.route('/leaderboard')
def index():
    return render_template('leaderboard/index.html')
