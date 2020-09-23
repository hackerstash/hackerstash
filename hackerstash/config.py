import os

config = {
    'host': os.environ.get('host'),
    'debug': os.environ.get('debug') == 'true',
    'secret': os.environ.get('secret'),

    # Database
    'sqlalchemy_database_uri': os.environ.get('sqlalchemy_database_uri'),
    'sqlalchemy_track_notifications': False,

    # Redis
    'redis_host': os.environ.get('redis_host'),
    'redis_port': os.environ.get('redis_port', 6379),

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
    'admin_api_key': os.environ.get('admin_api_key'),

    # Stripe
    'stripe_api_key': os.environ.get('stripe_api_key'),
    'stripe_api_secret_key': os.environ.get('stripe_api_secret_key'),
    'stripe_price_id': os.environ.get('stripe_price_id'),
    'stripe_success_uri': os.environ.get('stripe_success_uri'),
    'stripe_failure_uri': os.environ.get('stripe_failure_uri'),

    # Misc
    'app_environment': os.environ.get('app_environment', 'dev'),
    'error_webhook': os.environ.get('error_webhook')
}

