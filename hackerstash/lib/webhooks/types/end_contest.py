from hackerstash.lib.logging import Logging
from hackerstash.lib.webhooks.base import Base
from hackerstash.models.contest import Contest

log = Logging(module='Webhook::EndContest')


class EndContest(Base):
    def __init__(self, payload: dict) -> None:
        super().__init__(payload)

        month = payload.get('month')
        year = payload.get('year')

        log.info('Ending the contest', {'month': month, 'year': year})

        Contest.end(int(month) if month else None, int(year) if year else None)
