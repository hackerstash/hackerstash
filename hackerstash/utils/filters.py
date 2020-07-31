import arrow
import calendar
from markdown import markdown


def init_app(app):
    app.jinja_env.filters['to_markdown'] = to_markdown
    app.jinja_env.filters['to_human_date'] = to_human_date
    app.jinja_env.filters['to_named_month'] = to_named_month
    app.jinja_env.filters['nest_comments'] = nest_comments
    app.jinja_env.filters['platforms_and_devices'] = platforms_and_devices
    app.jinja_env.filters['business_models'] = business_models
    app.jinja_env.filters['fundings'] = fundings


def to_markdown(value):
    return markdown(value) if value else ''


def to_human_date(date):
    d = arrow.get(date)
    return d.humanize()


def to_named_month(month):
    index = int(month) + 1
    return calendar.month_name[index]


def nest_comments(comments, should_nest):
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


def platforms_and_devices(value):
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


def business_models(value):
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


def fundings(value):
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
