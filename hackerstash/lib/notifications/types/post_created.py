from hackerstash.lib.notifications.base import Base


class PostCreated(Base):
    def __init__(self, payload):
        super().__init__(payload)
