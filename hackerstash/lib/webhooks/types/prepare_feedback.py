import random
from hackerstash.db import db
from hackerstash.lib.logging import Logging
from hackerstash.lib.webhooks.base import Base
from hackerstash.models.feedback import Feedback
from hackerstash.models.project import Project

log = Logging(module='Webhook::PrepareFeedback')


class PrepareFeedback(Base):
    def __init__(self, payload: dict) -> None:
        """
        Initialise an instance of the PrepareFeedback class
        :param payload: dict
        """
        super().__init__(payload)

        log.info('Preparing feedback for this weeks goals')

        # Get all the projects that have a set of active goals
        projects = [project for project in Project.query.all() if len(project.active_goals)]
        # Shuffle the projects so you get a random bunch
        random.shuffle(projects)  # p.s. Python is fucking great isn't it, try this in JavaScript!
        # Limit the array so you get a max of 10
        projects = projects[:10]

        for project in projects:
            # Make sure you don't review yourself
            projects_to_review = [p for p in projects if p.id != project.id]

            # For each project you need to review, queue up the feedback
            for p in projects_to_review:
                feedback = Feedback(goals=p.active_goals, project=project)
                db.session.add(feedback)
                db.session.commit()
