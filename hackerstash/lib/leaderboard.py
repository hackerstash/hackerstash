import arrow
from datetime import datetime
from hackerstash.lib.logging import Logging
from hackerstash.lib.redis import redis

log = Logging(module='Leaderboard')


class Leaderboard:
    def __init__(self, project):
        """
        Initialise a new instance of the leaderboard class
        :param project:
        """
        self.project = project

    @classmethod
    def key(cls) -> str:
        now = datetime.now()
        return f'monthly_leaderboard:{now.month}:{now.year}'

    @classmethod
    def order(cls, reverse=False) -> list[int]:
        """
        Get the order of the leaderboard from redis and return
        the list of project ids
        :param reverse: bool
        :return: list[int]
        """
        # Get the order of ids in the leaderboard. By
        # default we return the ids in descending order
        # as that's the default order for the leaderboard
        if reverse:
            order = redis.zrange(cls.key(), 0, -1)
        else:
            order = redis.zrevrange(cls.key(), 0, -1)
        # Decode the ids from bytes and convert to ints
        return [int(x.decode('utf-8')) for x in order]

    @classmethod
    def remaining_days(cls) -> str:
        """
        Return how long until the tournament ends in a human
        readable format
        :return: str
        """
        return arrow.utcnow().ceil('month').humanize(only_distance=True)

    @property
    def position(self) -> int:
        """
        Get the position of a single project from the leaderboard. It
        will return it on a 1-index basis for human consumption
        :return: int
        """
        rank = redis.zrevrank(self.key(), self.project.id)
        return rank + 1 if rank is not None else -1

    @property
    def score(self) -> int:
        """
        Get the score of a single project from the leaderboard
        :return: int
        """
        score = redis.zscore(self.key(), self.project.id) or 0.0
        return int(score)

    def update(self, amount: int) -> int:
        """
        Update the projects score, the value can also be minus to deduct
        points. It will return the updated score.
        :param amount: int
        :return: int
        """
        score = redis.zincrby(self.key(), amount, self.project.id)
        log.info('Updating leaderboard', {'key': self.key(), 'amount': amount, 'new_score': int(score), 'project_id': self.project.id})
        return int(score)
