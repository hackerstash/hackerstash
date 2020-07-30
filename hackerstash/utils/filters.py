import arrow
from markdown import markdown


def to_markdown(value):
    if not value:
        return ''

    return markdown(value)


def to_human_date(date):
    d = arrow.get(date)
    return d.humanize()


def to_named_month(month):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    index = int(month)
    return months[index]
