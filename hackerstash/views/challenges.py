from flask import Blueprint, render_template, g
from hackerstash.utils.auth import login_required

challenges = Blueprint('challenges', __name__)


@challenges.route('/challenges')
@login_required
def index() -> str:
    challenge_status = {
        'post_created': 0,
        'comment_created': 0,
        'given_project_vote': 0,
        'given_post_vote': 0,
        'given_comment_vote': 0,
        'post_streak': 0,
        'received_post_vote': 0,
        'received_comment_vote': 0,
        'award_points': 0
    }
    challenge_list = g.user.member.project.challenges
    print(challenge_list)
    return render_template('challenges/index.html', challenge_status=challenge_status)
