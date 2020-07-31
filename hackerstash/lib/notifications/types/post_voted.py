from hackerstash.lib.notifications.base import Base


class PostVoted(Base):
    def __init__(self, payload):
        super().__init__(payload)
