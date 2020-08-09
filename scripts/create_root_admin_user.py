import boto3
from hackerstash.db import db
from hackerstash.server import app
from hackerstash.models.admin import Admin

client = boto3.client('ssm', region_name='eu-west-1')


def get_root_admin_password() -> str:
    response = client.get_parameter(Name='root_admin_user_password', WithDecryption=True)
    return response['Parameter']['Value']


def create_root_admin_user() -> None:
    password = get_root_admin_password()
    u = Admin(first_name='Rooty', last_name='McRootFace', email='hello@hackerstash.com', password=password, root=True)
    db.session.add(u)
    db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        db.init_app(app)
        create_root_admin_user()

        print('Created root admin user')
