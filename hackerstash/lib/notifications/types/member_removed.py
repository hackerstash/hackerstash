from hackerstash.lib.notifications.base import Base


class MemberRemoved(Base):
    def __init__(self, payload):
        super().__init__(payload)
