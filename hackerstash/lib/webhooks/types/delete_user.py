from hackerstash.db import db
from hackerstash.lib.logging import logging
from hackerstash.lib.webhooks.base import Base
from hackerstash.models.user import User


class DeleteUser(Base):
    def __init__(self, payload: dict) -> None:
        super().__init__(payload)

        logging.info('Deleting a user via the webhook')

        user_id = payload.get('user_id')
        user = User.query.get(user_id)

        if user:
            db.session.delete(user)
            db.session.commit()
