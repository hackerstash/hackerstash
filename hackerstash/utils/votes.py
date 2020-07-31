def sum_of_votes(votes):
    score = 0

    for vote in votes:
        score += vote.score

    return score


def sum_of_project_votes(project):
    score = sum_of_votes(project.votes)

    for post in project.posts:
        score += sum_of_votes(post.votes)

        for comment in post.comments:
            score += sum_of_votes(comment.votes)

    return score
