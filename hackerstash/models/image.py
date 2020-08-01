from hackerstash.db import db


class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)

    file_name = db.Column(db.String)
    key = db.Column(db.String)

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self):
        return f'<Image {self.file_name}>'
