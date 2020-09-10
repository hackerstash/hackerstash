from hackerstash.models.challenge import Challenge
from hackerstash.utils.contest import get_week_and_year


def is_this_week(date) -> bool:
    current_week, current_year = get_week_and_year()
    year, week, day = date.toisocalendar()
    return current_week == week and current_year == year


def sum_of_votes(votes, this_contest_only=True) -> int:
    score = 0
    for vote in votes:
        # Either:
        # - we want to show everything (!this_contest_only) or
        # - we want to show only this week and the stuff must match
        if not this_contest_only or this_contest_only and vote.is_current_contest:
            score += vote.score
    return score


def sum_of_weekly_challenges(project) -> int:
    completed = Challenge.get_completed_challenges_for_project(project)
    return sum(c.score for c in completed)


def sum_of_project_votes(project) -> int:
    score = 0

    score += sum_of_votes(project.votes)
    score += sum_of_weekly_challenges(project)

    # Tally up all the votes from the posts that
    # are owned by the project
    for post in project.posts:
        score += sum_of_votes(post.votes)

    # Tally up all the votes that are authored by
    # members of the project
    for member in project.members:
        for comment in member.user.comments:
            score += sum_of_votes(comment.votes)

    return score
