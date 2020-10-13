from hackerstash.lib.logging import Logging
from hackerstash.lib.webhooks.base import Base
from hackerstash.models.contest import Contest

log = Logging(module='Webhook::EndContest')


class EndContest(Base):
    def __init__(self, payload: dict) -> None:
        super().__init__(payload)

        week = payload.get('week')
        year = payload.get('year')

        log.info('Ending the contest', {'week': week, 'year': year})

        Contest.end(int(week) if week else None, int(year) if year else None)
