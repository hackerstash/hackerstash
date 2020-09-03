from hackerstash.db import db
from hackerstash.server import app
from hackerstash.lib.logging import logging
from hackerstash.models.contest import Contest
from hackerstash.utils.contest import get_week_and_year


def create_first_contest():
    week, year = get_week_and_year()
    c = Contest(week=week, year=year, tournament=1)
    db.session.add(c)
    db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        db.init_app(app)
        create_first_contest()
        logging.info('Created first tournament')
