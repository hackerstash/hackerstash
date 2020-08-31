import os

config = {
    'host': os.environ.get('host'),
    'debug': os.environ.get('debug') == 'true',
    'secret': os.environ.get('secret'),
    'sqlalchemy_database_uri': os.environ.get('sqlalchemy_database_uri'),
    'sqlalchemy_track_notifications': False,
    'redis_host': os.environ.get('redis_host'),
    'redis_port': os.environ.get('redis_port', 6379),
    'app_environment': os.environ.get('app_environment', 'dev'),
    'error_webhook': os.environ.get('error_webhook'),

    # reCaptcha
    'recaptcha_site_key': os.environ.get('recaptcha_site_key'),
    'recaptcha_secret_key': os.environ.get('recaptcha_secret_key'),

    # Google
    'google_api_key': os.environ.get('google_api_key'),
    'google_client_id': os.environ.get('google_client_id'),
    'google_client_secret': os.environ.get('google_client_secret'),

    # Twitter
    'twitter_api_key': os.environ.get('twitter_api_key'),
    'twitter_api_secret': os.environ.get('twitter_api_secret'),

    # Admin
    'admin_api_key': os.environ.get('admin_api_key')
}
