from hackerstash.db import db


class Invite(db.Model):
    __tablename__ = 'invites'

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String, unique=True)
    first_name = db.Column(db.String)
    link = db.Column(db.String)
    role = db.Column(db.String)

    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self) -> str:
        return f'<Invites {self.email}>'
