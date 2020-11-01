# HackerStash

### Requirements:
- Docker
- docker-compose
- AWS credentials at ~/.aws
- Python 3.9

### Installation:
Clone the repo:
```shell script
$ git@github.com:hackerstash/hackerstash.git
```
Set up the environment
```shell script
$ bin/init.sh
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
# Enter the container
$ docker-compose exec web sh

# Run all the migrations
$ flask db upgrade
```
