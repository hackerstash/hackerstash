import bcrypt
from hackerstash.db import db


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


class Admin(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    root = db.Column(db.Boolean, nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __init__(self, first_name: str, last_name: str, email: str, password: str, root: bool) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = hash_password(password)
        self.root = root

    def __repr__(self) -> str:
        return f'<Admin {self.first_name} {self.last_name}>'

    def validate_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
