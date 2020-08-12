import datetime
from hackerstash.db import db
from hackerstash.lib.logging import logging
from hackerstash.models.challenge import Challenge


def challenges_factory(key, user):
    now = datetime.datetime.now()
    week = datetime.date(now.year, now.month, now.day).isocalendar()[1] - 1
    year = now.year

    logging.info(key, week, year)

    pass
