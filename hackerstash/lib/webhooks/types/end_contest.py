from datetime import datetime
from sqlalchemy import func
from hackerstash.lib.logging import Logging
from hackerstash.lib.webhooks.base import Base
from hackerstash.lib.leaderboard import Leaderboard
from hackerstash.models.project import Project

log = Logging(module='Webhook::EndContest')


class EndContest(Base):
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
            .order_by(order_expr)

        # TODO: Sort out contest end stuff
        print(projects)
