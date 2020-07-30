import uuid
import boto3

client = boto3.client('s3', region_name='eu-west-1')


def upload_image(image):
    key = str(uuid.uuid4())

    params = {
        'Body': image,
        'Bucket': 'images.hackerstash.com',
        'Key': key
    }

    client.put_object(**params)
    return key


def delete_image(key):
    try:
        params = {
            'Bucket': 'images.hackerstash.com',
            'Key': key
        }

        client.delete_object(**params)
    except Exception as e:
        print(e)
        pass