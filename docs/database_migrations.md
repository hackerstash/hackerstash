# Database Migrations

We use Flask-Migrate to handle migrations, some background reading can be found here:

https://flask-migrate.readthedocs.io/en/latest/

Unlike Rails where you create the modal and the migration at the same time via the CLI, you first must create the model inside of hackerstash/models/, and then run the migration commands. Because we define all the columns, type and relations with SQL Alchemy, Flask-Migrate is able to infer all of these to automatically create the migration scripts.

### Example
Create a model:
```python
# hackerstash/models/foo.py

class Foo(db.Model):
    __tablename__ = 'foo'

    id = db.Column(db.Integer, primary_key=True)
    bar = db.Column(db.String)

``` 
Reference the model in the app:
```python
# hackerstash/path/to/your/file.py

from hackerstash.models.foo import Foo

```

Create the migration:
```shell script
$ flask db migrate -m "Add Foo model"
```

Run the migration:
```shell script
$ flask db upgrade
```