import arrow
import bleach
import calendar


def init_app(app):
    app.jinja_env.filters['to_safe_html'] = to_safe_html
    app.jinja_env.filters['to_plain_text'] = to_plain_text
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
    app.jinja_env.filters['to_currency'] = to_currency
    app.jinja_env.filters['to_nice_url'] = to_nice_url


def to_safe_html(value: str) -> str:
    # List of all allowed tags
    tags = ['h1', 'h2', 'h3', 'p', 'span', 'ul', 'ol', 'li', 'pre', 'a', 'img', 'strong', 'br', 'em', 'u', 's']
    # List of all allowed attributes for tags
    attrs = {'img': ['src'], 'a': ['href', 'data-preview', 'class']}
    return bleach.clean(value or '', tags=tags, attributes=attrs, strip=True)


def to_plain_text(value: str) -> str:
    return bleach.clean(value or '', tags=[], strip=True)


def to_human_date(date) -> str:
    d = arrow.get(date)
    return d.humanize()


def to_nice_date(date) -> str:
    d = arrow.get(date)
    return d.format('MMMM D [at] h:mmA')


def to_contest_date(date) -> str:
    d = arrow.get(date)
    return d.format('Do MMMM, YYYY')


def to_named_month(month) -> str:
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
        'android': 'Android',
        'browser_plugin': 'Browser Plugin',
        'desktop': 'Desktop',
        'ios': 'iOS',
        'mac': 'Mac',
        'mobile': 'Mobile',
        'pc': 'PC',
        'web': 'Web',
        'hardware': 'Hardware',
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
        'hackerstash': 'HackerStash',
        'self_funded': 'Self Funded',
        'vc_funded': 'VC Funded',
        'seed_funded': 'Seed Funded'
    }
    return items.get(value, value)


def to_ordinal_ending(number: int) -> str:
    return "tsnrhtdd"[(number / 10 % 10 != 1) * (number % 10 < 4) * number % 10::4]


def to_currency(number: int) -> str:
    return '${:,.2f}'.format(number)


def to_nice_url(url: str) -> str:
    return url.replace('https://', '').replace('http://', '').replace('www.', '')
