from hackerstash.db import db


class Waitlist(db.Model):
    __tablename__ = 'waitlist'

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self) -> str:
        return f'<Waitlist {self.first_name}>'

    @classmethod
    def create_is_not_exists(cls, **kwargs) -> None:
        if not cls.query.filter_by(email=kwargs['email']).first():
            obj = cls(**kwargs)
            db.session.add(obj)
            db.session.commit()
