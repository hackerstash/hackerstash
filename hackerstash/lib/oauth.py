from flask_dance.contrib.google import make_google_blueprint
from flask_dance.contrib.twitter import make_twitter_blueprint
from hackerstash.config import config

google_blueprint = make_google_blueprint(
    client_id=config['google_client_id'],
    client_secret=config['google_client_secret'],
    redirect_to='login.google_callback',
    scope='https://www.googleapis.com/auth/userinfo.profile openid https://www.googleapis.com/auth/userinfo.email'
)

twitter_blueprint = make_twitter_blueprint(
    api_key=config['twitter_api_key'],
    api_secret=config['twitter_api_secret'],
    redirect_to='login.twitter_callback'
)
