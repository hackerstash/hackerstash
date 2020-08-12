import datetime
from hackerstash.db import db
from hackerstash.lib.logging import logging


class Base:
    def __init__(self, payload: dict) -> None:
        self.payload = payload
        self.challenges_to_create = []

    @property
    def week(self) -> int:
        now = datetime.datetime.now()
        return datetime.date(now.year, now.month, now.day).isocalendar()[1] - 1

    @property
    def year(self) -> int:
        now = datetime.datetime.now()
        return now.year

    def create(self):
        for challenge in self.challenges_to_create:
            logging.info('Creating challenge', challenge)
            db.session.add(challenge)
        db.session.commit()
