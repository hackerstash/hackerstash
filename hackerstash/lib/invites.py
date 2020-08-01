import jwt
from flask import url_for
from hackerstash.config import config


def generate_invite_link(email):
    token = jwt.encode({'email': email}, config['secret'], algorithm='HS256')
    # jwt.encode returns bytes
    return config['host'] + url_for('projects.accept_invite', invite_token=token.decode('utf-8'))


def decrypt_invite_link(token):
    return jwt.decode(token, config['secret'], algorithm='HS256')
