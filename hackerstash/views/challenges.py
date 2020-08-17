import datetime
from flask import Blueprint, render_template, g
from hackerstash.utils.auth import login_required

challenges = Blueprint('challenges', __name__)


class ChallengeCount:
    def __init__(self, challenge_list):
        self.challenge_list = challenge_list

    def get_count_by_key(self, key: str) -> int:
        matches = list(filter(lambda x: x.key == key and x.week == self.week, self.challenge_list))
        return len(matches)

    @property
    def week(self):
        now = datetime.datetime.now()
        return datetime.date(now.year, now.month, now.day).isocalendar()[1] - 1


@challenges.route('/challenges')
@login_required
def index() -> str:
    challenge_count = ChallengeCount(g.user.member.project.challenges)

    challenge_status = {
        'post_created': challenge_count.get_count_by_key('post_created'),
        'comment_created': challenge_count.get_count_by_key('comment_created'),
        'given_project_vote': challenge_count.get_count_by_key('given_project_vote'),
        'given_post_vote': challenge_count.get_count_by_key('given_post_vote'),
        'given_comment_vote': challenge_count.get_count_by_key('given_comment_vote'),
        'post_streak': challenge_count.get_count_by_key('post_streak'),
        'received_post_vote': challenge_count.get_count_by_key('received_post_vote'),
        'received_comment_vote': challenge_count.get_count_by_key('received_comment_vote'),
        'award_points': challenge_count.get_count_by_key('award_points')
    }

    return render_template('challenges/index.html', challenge_status=challenge_status)
