import arrow
from datetime import datetime
from hackerstash.lib.logging import Logging
from hackerstash.lib.redis import redis

log = Logging(module='Leaderboard')


def key() -> str:
    now = datetime.now()
    return f'monthly_leaderboard:{now.month}:{now.year}'


class Leaderboard:
    key: str = key()

    def __init__(self, project):
        self.project = project

    @classmethod
    def order(cls, reverse=False) -> list[int]:
        # Get the order of ids in the leaderboard. By
        # default we return the ids in descending order
        # as that's the default order for the leaderboard
        if reverse:
            order = redis.zrange(cls.key, 0, -1)
        else:
            order = redis.zrevrange(cls.key, 0, -1)
        # Decode the ids from bytes and convert to ints
        return [int(x.decode('utf-8')) for x in order]

    @classmethod
    def remaining_days(cls) -> str:
        return arrow.utcnow().ceil('month').humanize(only_distance=True)

    @property
    def position(self) -> int:
        rank = redis.zrevrank(self.key, self.project.id)
        return rank + 1 if rank is not None else -1

    @property
    def score(self) -> int:
        score = redis.zscore(self.key, self.project.id) or 0.0
        return int(score)

    def update(self, amount: int) -> int:
        score = redis.zincrby(self.key, amount, self.project.id)
        log.info('Updating leaderboard', {'key': self.key, 'amount': amount, 'new_score': int(score), 'project_id': self.project.id})
        return int(score)
