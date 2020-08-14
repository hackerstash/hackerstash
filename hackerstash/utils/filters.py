import re
import arrow
import calendar
from markdown import markdown
from hackerstash.lib.logging import logging


def init_app(app):
    app.jinja_env.filters['to_markdown'] = to_markdown
    app.jinja_env.filters['to_human_date'] = to_human_date
    app.jinja_env.filters['to_nice_date'] = to_nice_date
    app.jinja_env.filters['to_contest_date'] = to_contest_date
    app.jinja_env.filters['to_named_month'] = to_named_month
    app.jinja_env.filters['nest_comments'] = nest_comments
    app.jinja_env.filters['flatten_comments'] = flatten_comments
    app.jinja_env.filters['platforms_and_devices'] = platforms_and_devices
    app.jinja_env.filters['business_models'] = business_models
    app.jinja_env.filters['fundings'] = fundings
    app.jinja_env.filters['to_ordinal_ending'] = to_ordinal_ending
    app.jinja_env.filters['to_post_body'] = to_post_body


def to_markdown(value: str) -> str:
    return markdown(value) if value else ''


def to_human_date(date) -> str:
    d = arrow.get(date)
    return d.humanize()


def to_nice_date(date) -> str:
    d = arrow.get(date)
    return d.format('MMMM D [at] h:mA')


def to_contest_date(date) -> str:
    d = arrow.get(date)
    return d.format('Do MMMM, YYYY')


def to_named_month(month) -> str:
    index = int(month) + 1
    return calendar.month_name[index]


def to_post_body(post) -> str:
    body = to_markdown(post.body)

    def build_image_url_from_filename(file_name):
        try:
            image = [i for i in post.images if i.file_name == file_name][0]
            return f'src="https://images.hackerstash.com/{image.key}"'
        except Exception as e:
            logging.error('Failed to render post body %', e)
            return 'src=""'

    return re.sub(r'src="(.*)"', lambda x: build_image_url_from_filename(x.group(1)), body)


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
        'android': 'Android',
        'browser_plugin': 'Browser Plugin',
        'desktop': 'Desktop',
        'ios': 'iOS',
        'mac': 'Mac',
        'mobile': 'Mobile',
        'pc': 'PC',
        'web': 'Web'
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
        'hackerstash': 'HackerStash',
        'self_funded': 'Self Funded',
        'vc_funded': 'VC Funded',
        'seed_funded': 'Seed Funded'
    }
    return items.get(value, value)


def to_ordinal_ending(number: int) -> str:
    return "tsnrhtdd"[(number / 10 % 10 != 1) * (number % 10 < 4) * number % 10::4]
