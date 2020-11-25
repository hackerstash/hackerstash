import boto3
from hackerstash.lib.logging import Logging

log = Logging(module='Emails::Base')
ses = boto3.client('ses', region_name='eu-west-1')


class Base:
    def __init__(self, email: str, payload: dict, sender='noreply') -> None:
        """
        Initialise an instance of the Email base class
        :param email: str
        :param payload: dict
        :param sender: str
        """
        self.email = email
        self.payload = payload
        self.sender = sender

    def send(self) -> None:
        """
        Send the email
        :return: None
        """
        log.info('Sending email', {'type': self.type, 'email': self.email})
        ses.send_email(**self.message)

    @property
    def message(self) -> dict:
        """
        Build the SES payload
        :return: dict
        """
        return {
            'Destination': {
                'ToAddresses': [self.email]
            },
            'Message': {
                'Body': {
                    'Html': {
                        'Charset': 'UTF-8',
                        'Data': self.body
                    },
                    'Text': {
                        'Charset': 'UTF-8',
                        'Data': self.text
                    }
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': self.subject
                }
            },
            'Source': f'HackerStash <{self.sender}@hackerstash.com>'
        }
