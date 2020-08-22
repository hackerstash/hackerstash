from sqlalchemy import text
from hackerstash.db import db
from hackerstash.utils.contest import get_week_and_year


def get_prize_data_for_position(position: int, prizes=None):
    # Kept getting circular dependency issues and can't be
    # arsed to look into it now
    prizes = prizes or get_prizes_without_importing_the_class()

    return {
        'value': prizes.get(f'prize_{position}', 0),
        'badge': get_badge_type_for_position(position)
    }


def get_prizes_without_importing_the_class():
    week, year = get_week_and_year()
    r = db.engine.execute(
        text('SELECT prizes from contests WHERE week=:week AND year=:year LIMIT 1'),
        {'week': week, 'year': year}
    )
    return [x[0] for x in r][0]


def get_badge_type_for_position(position: int):
    if position == 0:
        return 'gold'
    if position == 1:
        return 'silver'
    if position == 2:
        return 'bronze'
    if 2 < position < 8:
        return 'default'
    return None
