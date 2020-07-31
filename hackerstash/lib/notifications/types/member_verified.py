from hackerstash.lib.notifications.base import Base


class MemberVerified(Base):
    def __init__(self, payload):
        super().__init__(payload)
