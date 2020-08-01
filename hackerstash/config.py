import os

config = {
    'host': os.environ.get('host'),
    'debug': os.environ.get('debug'),
    'secret': os.environ.get('secret'),
    'sqlalchemy_database_uri': os.environ.get('sqlalchemy_database_uri'),
    'sqlalchemy_track_notifications': False,

    # Google
    'google_client_id': os.environ.get('google_client_id'),
    'google_client_secret': os.environ.get('google_client_secret')
}
