import datetime
from hackerstash.lib.challenges.counts import ChallengeCount
from hackerstash.utils.contest import get_week_and_year


class Base:
    def __init__(self, payload: dict) -> None:
        self.payload = payload

    @property
    def week(self) -> int:
        week, year = get_week_and_year()
        return week

    @property
    def year(self) -> int:
        now = datetime.datetime.now()
        return now.year

    def has_completed(self, project, key: str):
        challenge_counts = ChallengeCount(project.challenges)
        return challenge_counts.has_completed(key)
