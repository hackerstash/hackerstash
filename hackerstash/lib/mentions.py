import re
from flask import render_template_string
from hackerstash.lib.notifications.factory import notification_factory
from hackerstash.lib.logging import Logging
from hackerstash.models.user import User

log = Logging(module='Mentions')


class Mentions:
    def __init__(self, html: str) -> None:
        self.html = html
        self.mentions = []
        self.replacement = re.sub(r'@([a-z0-9\_\-\.])+', self.extract, html, flags=re.IGNORECASE)

    @property
    def body(self):
        return self.replacement

    def extract(self, match) -> str:
        mention, user = self.get_user(match.group(0))
        if user:
            self.mentions.append(user)
        return mention

    def get_user(self, mention: str) -> [str, User]:
        try:
            log.info(f'Trying to extract a mention', {'mention': mention})
            # The mention is already wrapped in an <a> tag. This
            # is likely because the post/comment is being updated
            if f'{mention}</a>' in self.html:
                return mention, None
            user = User.query.filter_by(username=mention.replace('@', '')).first()
            # The username is garbage and doesn't belong to a user
            if not user:
                return mention, None

            log.info('Found username within mention', {'user_id': user.id, 'mention': mention})
            # Return both the string and the user
            replr = '<a class="mention" href="{{ url_for(\'users.show\', user_id=user.id) }}">@{{ user.username }}</a>'
            return render_template_string(replr, user=user), user
        except Exception as e:
            log.error('Failed to extract mention', e)
            return mention, None

    def publish_post(self, post) -> None:
        mentioned = []
        for user in self.mentions:
            if user.id not in mentioned:
                mentioned.append(user.id)
                notification_factory('mention_created', {'user': user, 'post': post}).publish()

    def publish_comment(self, comment) -> None:
        mentioned = []
        for user in self.mentions:
            if user.id not in mentioned:
                mentioned.append(user.id)
                notification_factory('mention_created', {'user': user, 'comment': comment}).publish()
