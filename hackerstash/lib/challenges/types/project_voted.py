from flask import g
from hackerstash.lib.challenges.base import Base
from hackerstash.models.challenge import Challenge


class ProjectVoted(Base):
    def __init__(self, payload: dict) -> None:
        super().__init__(payload)

        user = g.user
        project = payload['project']

        if user.member.project_id != project.id:
            # TODO not existing
            challenge = Challenge(
                key='given_project_vote',
                week=self.week,
                year=self.year,
                project=user.member.project
            )
            self.challenges_to_create.append(challenge)

