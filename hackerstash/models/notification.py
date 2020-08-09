from hackerstash.db import db
from sqlalchemy.dialects.postgresql import JSON


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)

    type = db.Column(db.String)
    read = db.Column(db.Boolean, default=False)
    read_at = db.Column(db.DateTime)
    message = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self) -> str:
        return f'<Notification {self.id}>'
