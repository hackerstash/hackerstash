# Scripts

Running scripts is best done inside the Docker container where you have access to the enviornment variables.

### Running a script
```shell script
# Locally
$ docker-compose exec web bash
$ python -m 'scripts.<name_of_script>'

# Production
$ docker exec -ti <container_id> bash
$ python -m 'scripts.<name_of_script>'
```
