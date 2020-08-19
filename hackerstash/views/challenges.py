from flask import Blueprint, render_template, g
from hackerstash.lib.challenges.counts import ChallengeCount
from hackerstash.models.challenge import Challenge
from hackerstash.utils.auth import login_required

challenges = Blueprint('challenges', __name__)


@challenges.route('/challenges')
@login_required
def index() -> str:
    challenge_count = ChallengeCount(g.user.member.project.challenges)
    challenge_status = {}

    for key in challenge_count.challenge_types:
        challenge_status[key] = {
            'count': challenge_count.get_count_by_key(key),
            'complete': challenge_count.has_completed(key),
            'points': challenge_count.get_score_for_key(key),
            'max': Challenge.get_max_count_for(key)
        }

    return render_template('challenges/index.html', challenge_status=challenge_status)
