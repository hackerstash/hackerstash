import re
from flask import render_template_string
from hackerstash.lib.logging import logging
from hackerstash.models.user import User


def get_user_from_mention(html: str, mention: str) -> str:
    try:
        # The mention is already wrapped in an <a> tag. This
        # is likely because the post/comment is being updated
        if f'{mention}</a>' in html:
            return mention
        user = User.query.filter_by(username=mention.replace('@', '')).first()
        # The username is garbage and doesn't belong to a user
        if not user:
            return mention
        return render_template_string('<a class="mention" href="{{ url_for(\'users.show\', user_id=user.id) }}">@{{ user.username }}</a>', user=user)
    except Exception as e:
        logging.warning('Failed to extract mention: %s - %s', mention, e)
        return mention


def add_mentions(html):
    return re.sub(r'@([a-z0-9\_\-\.])+', lambda x: get_user_from_mention(html, x.group(0)), html, flags=re.IGNORECASE)
