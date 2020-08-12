from hackerstash.lib.challenges.types.comment_created import CommentCreated
from hackerstash.lib.challenges.types.comment_voted import CommentVoted
from hackerstash.lib.challenges.types.post_created import PostCreated
from hackerstash.lib.challenges.types.post_voted import PostVoted
from hackerstash.lib.challenges.types.project_voted import ProjectVoted


def challenge_factory(challenge_type: str, payload: dict):
    if challenge_type == 'comment_created':
        return CommentCreated(payload)
    if challenge_type == 'comment_voted':
        return CommentVoted(payload)
    if challenge_type == 'post_created':
        return PostCreated(payload)
    if challenge_type == 'post_voted':
        return PostVoted(payload)
    if challenge_type == 'project_voted':
        return ProjectVoted(payload)

    raise Exception(f'{challenge_type} is not a valid challenge type')
