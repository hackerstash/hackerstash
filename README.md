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

A sample .env file:
```
host=http://localhost
debug=true
secret=teapot
sqlalchemy_database_uri=postgresql://hackerstash:hackerstash@db:5432/hackerstash
google_client_id=
google_client_secret=
twitter_api_key=
twitter_api_secret=
```