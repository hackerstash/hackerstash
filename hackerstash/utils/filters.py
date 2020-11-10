import re
import json
import arrow
import bleach
import calendar
from flask import request, url_for, g
from hackerstash.utils.helpers import html_to_plain_text


def init_app(app):
    app.jinja_env.filters['to_safe_html'] = to_safe_html
    app.jinja_env.filters['to_plain_text'] = to_plain_text
    app.jinja_env.filters['to_human_date'] = to_human_date
    app.jinja_env.filters['to_nice_date'] = to_nice_date
    app.jinja_env.filters['to_feed_date'] = to_feed_date
    app.jinja_env.filters['to_named_month'] = to_named_month
    app.jinja_env.filters['nest_comments'] = nest_comments
    app.jinja_env.filters['flatten_comments'] = flatten_comments
    app.jinja_env.filters['platforms_and_devices'] = platforms_and_devices
    app.jinja_env.filters['business_models'] = business_models
    app.jinja_env.filters['fundings'] = fundings
    app.jinja_env.filters['to_ordinal_ending'] = to_ordinal_ending
    app.jinja_env.filters['to_nice_url'] = to_nice_url
    app.jinja_env.filters['paginate_to_page'] = paginate_to_page
    app.jinja_env.filters['paginate_in_feed'] = paginate_in_feed
    app.jinja_env.filters['truncate'] = truncate
    app.jinja_env.filters['winner_totals'] = winner_totals
    app.jinja_env.globals['call_to_action_state'] = call_to_action_state


def to_safe_html(value: str) -> str:
    # List of all allowed tags
    tags = ['h1', 'h2', 'h3', 'p', 'span', 'ul', 'ol', 'li', 'pre', 'a', 'img', 'strong', 'br', 'em', 'u', 's']
    # List of all allowed attributes for tags
    attrs = {'img': ['src'], 'a': ['href', 'data-preview', 'class', 'target', 'rel']}
    return bleach.clean(value or '', tags=tags, attributes=attrs, protocols=['data', 'http', 'https'], strip=True)


def to_plain_text(value: str) -> str:
    return html_to_plain_text(value)


def to_human_date(date) -> str:
    d = arrow.get(date)
    return d.humanize()


def to_nice_date(date) -> str:
    d = arrow.get(date)
    return d.format('MMMM D [at] h:mmA')


def to_feed_date(date) -> str:
    d = arrow.get(date)
    return d.format('MMMM D')


def to_named_month(month) -> str:
    if not month:
        return ''
    index = int(month) + 1
    return calendar.month_name[index]


def nest_comments(comments, should_nest: bool):
    if not should_nest:
        return comments

    def generate_nesting(array, parent=None):
        out = []
        for comment in array:
            if comment.parent_comment_id == parent:
                children = generate_nesting(array, comment.id)
                if len(children):
                    comment.children = children
                out.append(comment)
        return out
    return generate_nesting(comments)


def flatten_comments(comments):
    out = []

    for comment in comments:
        out.append(comment)
        children = getattr(comment, 'children', [])
        [out.append(x) for x in flatten_comments(children)]

    return out


def platforms_and_devices(value: str) -> str:
    items = {
        'android': 'Android App',
        'browser_plugin': 'Browser Plugin',
        'ios': 'iOS App',
        'mac': 'Mac App',
        'pc': 'PC App',
        'linux': 'Linux App',
        'web': 'Web App',
        'podcast': 'Podcast',
        'youtube': 'Youtube / Video',
        'newsletter': 'Newsletter',
        'hardware': 'Hardware',
        'website': 'Website',
        'other': 'Other'
    }
    return items.get(value, value)


def business_models(value: str) -> str:
    items = {
        'advertising': 'Advertising',
        'commission': 'Commission',
        'consulting': 'Consulting',
        'donations': 'Donations',
        'free': 'Free',
        'partnership': 'Partnership',
        'sales_and_transactions': 'Sales and Transactions',
        'subscriptions': 'Subscriptions'
    }
    return items.get(value, value)


def fundings(value: str) -> str:
    items = {
        'accelerator': 'Accelerator',
        'bootstrapped': 'Bootstrapped',
        'crowd_funded': 'Crowd Funded',
        'donation_supported': 'Donation Supported',
        'self_funded': 'Self Funded',
        'vc_funded': 'VC Funded',
        'seed_funded': 'Seed Funded'
    }
    return items.get(value, value)


def to_ordinal_ending(n: int) -> str:
    return "tsnrhtdd"[(n // 10 % 10 != 1) * (n % 10 < 4) * n % 10::4]


def to_nice_url(url: str) -> str:
    url = url.replace('https://', '').replace('http://', '').replace('www.', '')
    return re.sub(r'\/$', '', url)


def paginate_to_page(page: int = 0):
    # Splatting the page into the args is messy business
    # in the template!
    combined_args = {**request.args, **request.view_args, **{'page': page}}
    return url_for(request.endpoint, **combined_args)


def paginate_in_feed(page: int = 0):
    show = request.args.getlist('show')
    combined_args = {**request.view_args, 'show': show, 'page': page}
    return url_for('projects.feed', **combined_args)


def truncate(text: str, count: int):
    if not text:
        return ''
    if len(text) > count:
        return text[:count] + '...'
    return text


def winner_totals(winners: list) -> str:
    out = {}
    for w in winners:
        out[w.position] = out.get(w.position, 0)
        out[w.position] += 1
    return json.dumps(out)


def call_to_action_state():
    if 'user' not in g:
        return 'disabled logged-out'
    if g.user and not g.user.can_post:
        return 'disabled not-published'
    return ''
