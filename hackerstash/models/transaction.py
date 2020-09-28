from hackerstash.db import db
from hackerstash.lib.logging import logging


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)

    type = db.Column(db.String, nullable=False)
    value = db.Column(db.Integer, nullable=False)
    tournament_name = db.Column(db.String)

    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self) -> str:
        return f'<Transaction {self.id}>'

    # The default order should be newest first
    __mapper_args__ = {
        'order_by': created_at.desc()
    }

    @classmethod
    def add_prize_winnings(cls, past_result):
        logging.info(f'Adding prize transaction for \'{past_result.project.name}\' - ${past_result.prize}')
        tournament_name = f'{past_result.contest.year}.{past_result.contest.week}'
        # Increase their stash
        past_result.project.add_funds(past_result.prize['value'])
        # Record the transaction
        transaction = cls(
            type='prize',
            value=past_result.prize['value'],
            tournament_name=tournament_name,
            project=past_result.project
        )
        db.session.add(transaction)
        db.session.commit()
