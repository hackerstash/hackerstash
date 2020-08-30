# HackerStash

### Requirements:
- Docker
- docker-compose
- AWS credentials at ~/.aws
- Python 3.8

### Installation:
Clone the repo:
```shell script
$ git@github.com:hackerstash/hackerstash.git
```
Create the .env file
```shell script
$ touch .env # Fill in the values
```
Build the image
```shell script
$ docker-compose build
```

### Running the app
```shell script
$ docker-compose up
```

### Setup Database
```shell script
$ flask db upgrade
$ python -m 'scripts.create_current_tournament'
```

A sample .env file:
```
host=http://localhost
debug=true
secret=teapot
sqlalchemy_database_uri=postgresql://hackerstash:hackerstash@db:5432/hackerstash
redis_host=db
recaptcha_site_key=
recaptcha_secret_key=
google_api_key=
google_client_id=
google_client_secret=
twitter_api_key=
twitter_api_secret=
admin_api_key=teapot
OAUTHLIB_INSECURE_TRANSPORT=true
```