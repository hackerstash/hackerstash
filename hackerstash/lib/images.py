import io
import uuid
import boto3
import requests
from hackerstash.config import config
from hackerstash.lib.logging import logging

client = boto3.client('s3', region_name='eu-west-1')


def upload_image(image) -> str:
    key = str(uuid.uuid4())

    environment = config['app_environment']
    if environment != 'live':
        key = environment + '/' + key

    params = {
        'Body': image,
        'Bucket': 'images.hackerstash.com',
        'Key': key
    }

    client.put_object(**params)
    return key


def upload_image_from_url(url: str):
    try:
        r = requests.get(url, stream=True)
        r.raise_for_status()
        return upload_image(r.raw.read())
    except Exception as e:
        logging.error('Failed to upload remote image %s', e)
        return None


def delete_image(key: str) -> None:
    try:
        params = {
            'Bucket': 'images.hackerstash.com',
            'Key': key
        }

        client.delete_object(**params)
    except Exception as e:
        logging.error('Failed to delete image %s', e)
        pass
