from datetime import datetime
from sqlalchemy import func
from hackerstash.db import db
from hackerstash.lib.logging import Logging
from hackerstash.lib.webhooks.base import Base
from hackerstash.lib.leaderboard import Leaderboard
from hackerstash.lib.notifications.factory import notification_factory
from hackerstash.models.project import Project
from hackerstash.models.winner import Winner

log = Logging(module='Webhook::EndContest')


class EndContest(Base):
    """
    Initialise an instance of the EndContest class
    :param payload: dict
    """
    def __init__(self, payload: dict) -> None:
        super().__init__(payload)

        now = datetime.now()
        month = payload.get('month', now.month)
        year = payload.get('year', now.year)

        log.info('Ending the contest', {'month': month, 'year': year})
        order = Leaderboard.order()
        order_expr = func.array_position(order, Project.id)

        projects = Project.query \
            .filter(Project.id.in_(order)) \
            .filter(Project.published == True) \
            .order_by(order_expr)\
            .limit(3)\
            .all()

        for project in projects:
            if 0 < project.position < 4:
                winner = Winner(position=project.position, project=project)
                notification_factory('prize_awarded', {'project': project}).publish()
                db.session.add(winner)
        db.session.commit()

