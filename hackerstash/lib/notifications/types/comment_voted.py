from hackerstash.lib.notifications.base import Base


class CommentVoted(Base):
    def __init__(self, payload):
        super().__init__(payload)
