import re
from flask import render_template_string
from hackerstash.lib.notifications.factory import notification_factory
from hackerstash.lib.logging import Logging
from hackerstash.models.user import User

log = Logging(module='Mentions')


def get_user_from_mention(html: str, mention: str):
    try:
        log.info(f'Trying to extract a mention', {'mention': mention})
        # The mention is already wrapped in an <a> tag. This
        # is likely because the post/comment is being updated
        if f'{mention}</a>' in html:
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


def proccess_mentions(html):
    mentioned_users = []

    def replace_mentions(x):
        r, user = get_user_from_mention(html, x.group(0))
        if user:
            mentioned_users.append(user)
        return r

    replacement = re.sub(r'@([a-z0-9\_\-\.])+', replace_mentions, html, flags=re.IGNORECASE)
    return replacement, mentioned_users


def publish_post_mentions(users, post):
    mentioned = []
    for user in users:
        if user.id not in mentioned:
            mentioned.append(user.id)
            notification_factory('mention_created', {'user': user, 'post': post}).publish()


def publish_comment_mentions(users, comment):
    mentioned = []
    for user in users:
        if user.id not in mentioned:
            mentioned.append(user.id)
            notification_factory('mention_created', {'user': user, 'comment': comment}).publish()
