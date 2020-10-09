import arrow
from hackerstash.lib.logging import logging
from hackerstash.lib.redis import redis
from hackerstash.models.contest import Contest
from hackerstash.models.project import Project


class Sidebar:
    sidebar_cache_time = 60 * 10  # Ten minutes
    redis_cache_key = 'sidebar'

    def __init__(self):
        self.no_current_contest = False

    @property
    def prize_pool(self):
        return self.get_prize_pool

    @property
    def time_remaining(self):
        return arrow.utcnow().ceil('week').humanize(only_distance=True)

    @classmethod
    def clear_cache(cls):
        redis.delete(cls.redis_cache_key)

    @property
    def get_prize_pool(self):
        if cached := redis.get(self.redis_cache_key):
            return cached.decode('utf-8')
        else:
            count = Project.query.filter_by(published=True).count() * 2
            contest = Contest.get_current()

            if not contest:
                self.no_current_contest = True
                return '$N/A'

            prize = f'${count + contest.top_up}'
            return self.cache_prize_pool(prize)

    def cache_prize_pool(self, prize: str):
        logging.info('Caching sidebar data for 10 minutes')
        redis.set(self.redis_cache_key, prize, ex=self.sidebar_cache_time)
        return prize
