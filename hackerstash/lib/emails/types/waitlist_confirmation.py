from flask import render_template
from hackerstash.config import config
from hackerstash.lib.emails.base import Base


class WaitlistConfirmation(Base):
    def __init__(self, email: str, payload: dict) -> None:
        super().__init__(email, payload, 'hello')

    @property
    def type(self) -> str:
        return 'WAITLIST_CONFIRMATION'

    @property
    def body(self) -> str:
        return render_template('emails/waitlist_confirmation.html', **self.payload, host=config['host'])

    @property
    def text(self) -> str:
        return f'''
          Hi {self.payload['first_name']},
          Thanks so much for joining the HackerStash waitlist 😍!
          It's not long now until we launch, but in the mean time we'll keep you updated on our progress via email. If you have any questions or ideas for us then please don't hesitate to respond to this email, or reach out to chris@hackerstash.com.
          We can't wait to invite you to sign in to HackerStash for the first time and to help you and the community fund your projects 💸. If you know anyone else that might be excited about HackerStash then please spread the word 😊.
          Kind Regards, 
          The HackerStash Team
        '''

    @property
    def subject(self) -> str:
        return 'Thanks for joining the HackerStash waitlist 😇'
