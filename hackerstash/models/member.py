from hackerstash.db import db


class Member(db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True)

    owner = db.Column(db.Boolean, default=False)
    role = db.Column(db.String)

    user = db.relationship('User', backref='user', uselist=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project_id'), nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self):
        return f'<Member {self.id}>'