# Admin Console

The app includes an admin interface to manage some common tasks and view data.

Before it can be used, a root user must be created:
```shell script
# Locally
$ docker-compose exec web sh
$ python -m 'scripts.create_root_user'

# Production
$ docker exec -ti <container_id> sh
$ python -m 'scripts.create_root_user'
```

You can now login with the email and password:
Email: hello@hackerstash.com
Password: <value of ssm paramter>

With this user you can create your own user account. You probably shouldn't be using the root user!