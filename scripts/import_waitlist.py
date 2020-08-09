import boto3
from hackerstash.db import db
from hackerstash.server import app
from hackerstash.models.waitlist import Waitlist

client = boto3.client('dynamodb', region_name='eu-west-1')


def get_waitlist():
    params = {
        'TableName': 'waitlist'
    }
    response = client.scan(**params)
    return [deserialize_dynamodb_types(x) for x in response['Items']]


def deserialize_dynamodb_types(dynamo_dict: dict) -> dict:
    boto3.resource('dynamodb', region_name='eu-west-1')
    deserializer = boto3.dynamodb.types.TypeDeserializer()
    return {k: deserializer.deserialize(v) for k, v in dynamo_dict.items()}


def insert_to_pg(records):
    for r in records:
        w = Waitlist(first_name=r['first_name'], email=r['email'])
        db.session.add(w)
    db.session.commit()
    return records


if __name__ == '__main__':
    with app.app_context():
        db.init_app(app)

        waitlist = get_waitlist()
        waitlist = insert_to_pg(waitlist)

        print(f'Inserted {len(waitlist)} records')
