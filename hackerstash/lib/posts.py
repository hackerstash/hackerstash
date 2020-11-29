from flask import g
from hackerstash.db import db
from hackerstash.lib.challenges.factory import challenge_factory
from hackerstash.lib.notifications.factory import notification_factory
from hackerstash.lib.mentions import Mentions
from hackerstash.models.poll import Poll
from hackerstash.models.post import Post
from hackerstash.models.tag import Tag


class Posts:
    def __init__(self, title: str, body: str, tag_id: str):
        """
        Initialise a new posts class
        :param title: str
        :param body: str
        :param tag_id: str
        """
        self.title = title
        self.body = body
        self.tag = Tag.query.get(tag_id) if tag_id else None
        self.user = g.user
        self.poll = None
        self.mentions = Mentions(self.body)
        self.url_slug = Post.generate_url_slug(title)

        self.post = Post(
            title=self.title,
            body=self.mentions.body,
            user=self.user,
            url_slug=self.url_slug,
            tag=self.tag,
            project=self.user.project
        )

    def create(self):
        """
        Create a new post and dispatch the necessary notifications
        and challenges
        :return: None
        """
        db.session.add(self.post)
        db.session.commit()
        self.mentions.publish_post(self.post)
        challenge_factory('post_created', {'post': self.post})
        notification_factory('post_created', {'post': self.post}).publish()
        db.session.commit()

    def add_poll(self, question: str, choices):
        """
        Create a new poll and link it to the current post
        :param question: str
        :param choices:
        :return: None
        """
        self.poll = Poll(question, choices, self.post)
        db.session.add(self.poll)
