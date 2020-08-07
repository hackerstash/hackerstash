# Scripts

Running scripts is best done inside the Docker container where you have access to the enviornment variables.

### Running a script
```shell script
# Locally
$ docker-compose exec web sh
$ python -m 'scripts.import_waitlist'

# Production
$ docker exec -ti <container_id> sh
$ python -m 'scripts.import_waitlist'
```
