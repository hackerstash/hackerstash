import datetime
from hackerstash.lib.challenges.counts import ChallengeCount


class Base:
    def __init__(self, payload: dict) -> None:
        self.payload = payload

    @property
    def week(self) -> int:
        now = datetime.datetime.now()
        return datetime.date(now.year, now.month, now.day).isocalendar()[1] - 1

    @property
    def year(self) -> int:
        now = datetime.datetime.now()
        return now.year

    def has_completed(self, project, key: str):
        challenge_counts = ChallengeCount(project.challenges)
        return challenge_counts.has_completed(key)
