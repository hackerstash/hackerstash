from flask import Blueprint, render_template, g, session
from hackerstash.models.challenge import Challenge
from hackerstash.lib.challenges.helpers import challenge_types, get_max_count_for_key, get_score_for_key
from hackerstash.lib.redis import redis
from hackerstash.utils.auth import login_required
from hackerstash.utils.helpers import find_in_list

challenges = Blueprint('challenges', __name__)


@challenges.route('/challenges')
@login_required
def index() -> str:
    weekly_challenges = Challenge.get_weekly_challenges_for_project(g.user.member.project)
    challenge_status = {}

    for key in challenge_types:
        c = find_in_list(weekly_challenges, lambda x: x and x.key == key)
        challenge_status[key] = {
            'count': c.count if c else 0,
            'complete': c.complete if c else 0,
            'points': get_score_for_key(key),
            'max': get_max_count_for_key(key)
        }

    return render_template('challenges/index.html', challenge_status=challenge_status)


@challenges.route('/challenges/dismiss')
@login_required
def dismiss():
    redis.delete(f'{g.user.member.project.id}:challenge_completed')
    return '', 204
