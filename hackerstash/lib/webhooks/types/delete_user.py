from hackerstash.db import db
from hackerstash.lib.logging import Logging
from hackerstash.lib.webhooks.base import Base
from hackerstash.models.user import User

log = Logging('Webhook::DeleteUser')


class DeleteUser(Base):
    def __init__(self, payload: dict) -> None:
        """
        Initialise an instance of the DeleteUser class
        :param payload: dict
        """
        super().__init__(payload)

        user_id = payload.get('user_id')
        user = User.query.get(user_id)

        log.info('Deleting a user via the webhook', {'user_id': user_id})

        if user:
            db.session.delete(user)
            db.session.commit()
