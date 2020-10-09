from hackerstash.lib.logging import logging
from hackerstash.lib.webhooks.base import Base
from hackerstash.models.contest import Contest


class EndContest(Base):
    def __init__(self, payload: dict) -> None:
        super().__init__(payload)

        logging.info('Ending the contest via the webhook')

        week = payload.get('week')
        year = payload.get('year')

        Contest.end(int(week) if week else None, int(year) if year else None)
