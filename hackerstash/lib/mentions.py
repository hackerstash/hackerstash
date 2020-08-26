import re
from flask import render_template_string
from hackerstash.lib.logging import logging
from hackerstash.models.user import User


def get_user_from_mention(mention: str) -> str:
    try:
        username = mention.replace('@', '')
        user = User.query.filter_by(username=username).first()
        if not user:
            return mention

        return render_template_string('<a class="mention preview" data-preview="{{ user.preview_json }}" href="{{ url_for(\'users.show\', user_id=user.id) }}">@{{ user.username }}</a>', user=user)
    except Exception as e:
        logging.warning('Failed to extract mention: %s - %s', mention, e)
        return mention


def add_mentions(html):
    return re.sub(r'@([a-z0-9\_\-\.])+', lambda x: get_user_from_mention(x.group(0)), html, flags=re.IGNORECASE)
