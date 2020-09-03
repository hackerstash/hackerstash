from hackerstash.db import db
from hackerstash.server import app
from hackerstash.lib.logging import logging
from hackerstash.models.contest import PastResult
from hackerstash.models.transaction import Transaction


if __name__ == '__main__':
    with app.app_context():
        db.init_app(app)

        for past_result in PastResult.query.all():
            if past_result.project:
                tournament_name = f'{past_result.contest.year}.{past_result.contest.week}'
                exists = Transaction.query.filter_by(tournament_name=tournament_name, project_id=past_result.project.id).first()
                if exists:
                    logging.info('Skipping as they already have thier winnings')
                else:
                    Transaction.add_prize_winnings(past_result)
