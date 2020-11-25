import uuid
import boto3
import requests
from typing import BinaryIO
from hackerstash.config import config
from hackerstash.lib.logging import Logging

log = Logging(module='Images')
client = boto3.client('s3', region_name='eu-west-1')


class Images:
    @classmethod
    def upload(cls, image: BinaryIO) -> str:
        """
        Upload an image to S3 adn return the key that it was
        stored agaist
        :param image: BinaryIO
        :return: str
        """
        key = str(uuid.uuid4())
        # Prefix the key with the stage so that we have an easier
        # time seperating dev data from prod
        if environment := config['app_environment']:
            key = f'{environment}/{key}'

        params = {
            'Body': image,
            'Bucket': 'images.hackerstash.com',
            'Key': key
        }

        client.put_object(**params)
        return key

    @classmethod
    def upload_from_url(cls, url: str) -> str:
        """
        Upload an image from a remote url. This is useful when a user
        signs up with Google/Twitter as we can carry their profile image
        over
        :param url: str
        :return: str
        """
        try:
            r = requests.get(url, stream=True)
            r.raise_for_status()
            return cls.upload(r.raw.read())
        except Exception as e:
            log.error('Failed to upload image', e)

    @classmethod
    def delete(cls, key: str) -> None:
        """
        Delete an image from S3. It should not raise so that we don't block
        form submissions
        :param key: str
        :return: None
        """
        try:
            params = {
                'Bucket': 'images.hackerstash.com',
                'Key': key
            }
            client.delete_object(**params)
        except Exception as e:
            log.error('Failed to delete image', e)
