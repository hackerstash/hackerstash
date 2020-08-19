from hackerstash.lib.challenges.counts import ChallengeCount


def sum_of_votes(votes) -> int:
    score = 0

    for vote in votes:
        score += vote.score

    return score


def sum_of_weekly_challenges(challenges) -> int:
    score = 0
    challenge_counts = ChallengeCount(challenges)

    for key in challenge_counts.challenge_types:
        if challenge_counts.has_completed(key):
            score += challenge_counts.get_score_for_key(key)

    return score


def sum_of_project_votes(project) -> int:
    score = 0

    score += sum_of_votes(project.votes)
    score += sum_of_weekly_challenges(project.challenges)

    for post in project.posts:
        score += sum_of_votes(post.votes)

        for comment in post.comments:
            score += sum_of_votes(comment.votes)

    return score
