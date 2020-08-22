from hackerstash.db import db
from sqlalchemy.types import ARRAY


class ProgressSetting(db.Model):
    __tablename__ = 'progress_settings'

    id = db.Column(db.Integer, primary_key=True)

    enabled = db.Column(db.Boolean)
    columns = db.Column(ARRAY(db.String))

    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self) -> str:
        return f'<ProgressSetting {self.project.id}>'

    def column_has_children(self, column: str):
        matches = list(filter(lambda x: x.column == column, self.project.progress))
        return len(matches) > 0
