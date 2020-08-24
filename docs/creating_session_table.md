# Creating Session Table

Currently we store our sessions in the database because we haven't set up redis yet.

To create the table you need to do the following:

Exec into the container:
```
# Dev:
$ docker-compose exec web sh
# Live:
$ docker exec -ti <id> sh
```
Enter the flask shell:
```
$ flask shell
```
Create the table:
```
>>> from flask_session import Session
>>> from hackerstash.server import session
>>> session = Session(app)
>>> session.app.session_interface.db.create_all()
```

**NOTE:**

You may need to change the column from VARCHAR 250 to plain old VARCHAR