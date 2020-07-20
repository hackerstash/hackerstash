from hackerstash.db import db


class Tokens(db.Model):
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String, unique=True, nullable=False)
    token = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self):
        return f'<Token {self.email}>'
