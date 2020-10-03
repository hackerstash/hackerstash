import uuid
import boto3
import requests
from hackerstash.config import config
from hackerstash.lib.logging import logging

client = boto3.client('s3', region_name='eu-west-1')


class Images:
    @classmethod
    def upload(cls, image) -> str:
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

    @classmethod
    def upload_from_url(cls, url: str):
        try:
            r = requests.get(url, stream=True)
            r.raise_for_status()
            return cls.upload(r.raw.read())
        except Exception as e:
            logging.stack(e)

    @classmethod
    def delete(cls, key: str):
        try:
            params = {
                'Bucket': 'images.hackerstash.com',
                'Key': key
            }
            client.delete_object(**params)
        except Exception as e:
            logging.stack(e)
