if [ ! -f ".env" ]; then
  echo "Creating env file..."
  cat >> ".env" << EOF
host=http://localhost:5000
debug=true
secret=teapot
sqlalchemy_database_uri=postgresql://hackerstash:hackerstash@db:5432/hackerstash
sqlalchemy_echo=false
recaptcha_site_key=
recaptcha_secret_key=
google_api_key=
google_client_id=
google_client_secret=
twitter_api_key=
twitter_api_secret=
redis_host=redis
stripe_api_key=
stripe_api_secret_key=
stripe_price_id=
stripe_success_uri=http://localhost:5000/stripe/checkout/success
stripe_failure_uri=http://localhost:5000/stripe/checkout/failure

FLASK_ENV=development
PYTHONUNBUFFERED=1
OAUTHLIB_INSECURE_TRANSPORT=true
EOF
fi