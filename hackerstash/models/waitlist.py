from hackerstash.db import db


class Waitlist(db.Model):
    __tablename__ = 'waitlist'

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self):
        return f'<Waitlist {self.first_name}>'
