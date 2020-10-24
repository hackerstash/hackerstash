import datetime
from hackerstash.models.challenge import Challenge


class Base:
    def __init__(self, payload: dict) -> None:
        self.payload = payload

    @property
    def month(self) -> int:
        now = datetime.datetime.now()
        return now.month

    @property
    def year(self) -> int:
        now = datetime.datetime.now()
        return now.year

    def has_completed(self, project, key: str):
        return Challenge.has_completed_key(project, key)
