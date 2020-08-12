from flask import g
from hackerstash.lib.challenges.base import Base
from hackerstash.models.challenge import Challenge


class CommentVoted(Base):
    def __init__(self, payload: dict) -> None:
        super().__init__(payload)

        user = g.user
        comment = payload['comment']

        if comment.post.project.id != user.member.project.id:
            # challenge = Challenge(
            #     key='have_your_comment_upvoted_by_competitors',
            #     week=self.week,
            #     year=self.year,
            #     project=comment.post.project
            # )
            # self.challenges_to_create.append(challenge)
            pass
