import uuid
import boto3
from hackerstash.lib.logging import logging

client = boto3.client('s3', region_name='eu-west-1')


def upload_image(image) -> str:
    key = str(uuid.uuid4())

    params = {
        'Body': image,
        'Bucket': 'images.hackerstash.com',
        'Key': key
    }

    client.put_object(**params)
    return key


def delete_image(key: str) -> None:
    try:
        params = {
            'Bucket': 'images.hackerstash.com',
            'Key': key
        }

        client.delete_object(**params)
    except Exception as e:
        logging.error('Failed to delete image %', e)
        pass
