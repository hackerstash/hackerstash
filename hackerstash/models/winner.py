from hackerstash.db import db


class Winner(db.Model):
    __tablename__ = 'winners'

    id = db.Column(db.Integer, primary_key=True)

    position = db.Column(db.Integer, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self) -> str:
        return f'<Winners {self.id}>'
