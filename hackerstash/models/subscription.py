from datetime import datetime
from hackerstash.db import db


class Subscription(db.Model):
    __tablename__ = 'subscriptions'

    id = db.Column(db.Integer, primary_key=True)

    invoice_id = db.Column(db.String)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    total = db.Column(db.Integer)
    receipt_url = db.Column(db.String)

    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self) -> str:
        return f'<Subscription {self.id}>'

    # The default order should be newest first
    __mapper_args__ = {
        'order_by': created_at.desc()
    }

    @classmethod
    def create_with_stripe_event(cls, event, project):
        period = event['lines']['data'][0]['period']

        cls(
            invoice_id=event['id'],
            start_date=datetime.fromtimestamp(period['start']),
            end_date=datetime.fromtimestamp(period['end']),
            total=int(event['amount_paid'] / 100),
            receipt_url=event['hosted_invoice_url'],
            project=project
        )
