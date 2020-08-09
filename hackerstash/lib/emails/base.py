import boto3

ses = boto3.client('ses', region_name='eu-west-1')


class Base:
    def __init__(self, email: str, payload: dict, sender='noreply'):
        self.email = email
        self.payload = payload
        self.sender = sender

    def send(self) -> None:
        print(f'Sending {self.type} email to {self.email}')
        ses.send_email(**self.message)

    @property
    def message(self) -> dict:
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
