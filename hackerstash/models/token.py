from random import randint
from hackerstash.db import db


class Token(db.Model):
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String, unique=True, nullable=False)
    token = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self) -> str:
        return f'<Token {self.email}>'

    @classmethod
    def generate(cls, email: str) -> int:
        code = randint(100000, 999999)
        existing = cls.query.filter_by(email=email).first()

        if existing:
            existing.token = code
        else:
            token = cls(email=email, token=code)
            db.session.add(token)

        db.session.commit()
        return code

    @classmethod
    def verify(cls, email: str, code: str) -> bool:
        token = cls.query.filter_by(email=email).first()
        return token.token == int(code) if token else False

    @classmethod
    def delete(cls, email: str) -> None:
        token = cls.query.filter_by(email=email).first()
        db.session.delete(token)
        db.session.commit()
