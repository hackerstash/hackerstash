from hackerstash.db import db
from hackerstash.utils.prizes import get_prize_data_for_position


class PastResult(db.Model):
    __tablename__ = 'past_results'

    id = db.Column(db.Integer, primary_key=True)

    rank = db.Column(db.Integer)
    score = db.Column(db.Integer)

    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    contest_id = db.Column(db.Integer, db.ForeignKey('contests.id'), nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self) -> str:
        return f'<PastResult {self.id}>'

    @property
    def prize(self):
        return get_prize_data_for_position(self.rank, self.contest.prizes)

    @property
    def position(self):
        return self.rank + 1
