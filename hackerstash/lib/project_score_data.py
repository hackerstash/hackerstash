import arrow
import datetime
from calendar import monthrange


def build_monthly_vote_data(project):
    out = []
    now = datetime.datetime.now()
    start_of_month = arrow.now().floor('month')
    day_range = monthrange(now.year, now.month)
    for i in range(day_range[1]):
        this_day = start_of_month.shift(days=+i)
        out.append(get_vote_score_by_day(project, this_day) + get_challenge_score_by_day(project, this_day))
    return out


def is_same_day(first_date, second_date):
    return first_date.isocalendar() == second_date.isocalendar()


def get_completed_challenges_for_day(challenges, date):
    out = []
    for c in challenges:
        if is_same_day(c.created_at, date) and c.complete:
            out.append(c)
    return out


def get_vote_score_by_day(project, date) -> int:
    votes = list(filter(lambda x: is_same_day(x.created_at, date), project.all_votes))
    return sum(vote.score for vote in votes)


def get_challenge_score_by_day(project, date) -> int:
    challenges = get_completed_challenges_for_day(project.challenges, date)
    return sum(challenge.score for challenge in challenges)
