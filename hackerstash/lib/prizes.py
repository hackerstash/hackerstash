import json
from sqlalchemy import text
from hackerstash.db import db
from hackerstash.lib.logging import Logging
from hackerstash.lib.redis import redis
from hackerstash.utils.contest import get_week_and_year

log = Logging(module='Prizes')


class Prizes:
    sidebar_cache_time = 60 * 10  # Ten minutes
    redis_cache_key = 'prizes'

    @classmethod
    def get_for_position(cls, position: int, prizes=None):
        # Kept getting circular dependency issues and can't be
        # arsed to look into it now
        prizes = prizes or cls.get_prizes()
        return {
            'value': prizes.get(f'prize_{position}', 0),
            'badge': cls.get_badge_type_for_position(position)
        }

    @classmethod
    def get_prizes(cls):
        if cached := redis.get(cls.redis_cache_key):
            return json.loads(cached)
        else:
            week, year = get_week_and_year()
            r = db.engine.execute(
                text('SELECT prizes from contests WHERE week=:week AND year=:year LIMIT 1'),
                {'week': week, 'year': year}
            )
            return cls.cache_prizes([x[0] for x in r][0])

    @classmethod
    def cache_prizes(cls, prizes):
        log.info('Caching prize data for 5 minutes')
        redis.set(cls.redis_cache_key, json.dumps(prizes), ex=cls.sidebar_cache_time)
        return prizes

    @classmethod
    def get_badge_type_for_position(cls, position: int):
        if position == 0:
            return 'gold'
        if position == 1:
            return 'silver'
        if position == 2:
            return 'bronze'
        if 2 < position < 8:
            return 'default'
        return None
