import os

config = {
    'host': os.environ.get('HOST'),
    'debug': os.environ.get('DEBUG'),
    'secret': os.environ.get('SECRET'),
    'SQLALCHEMY_DATABASE_URI': os.environ.get('SQLALCHEMY_DATABASE_URI'),
    'SQLALCHEMY_TRACK_MODIFICATIONS': False
}
