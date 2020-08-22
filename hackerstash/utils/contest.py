import datetime


def get_week_and_year():
    now = datetime.datetime.now()
    week = datetime.date(now.year, now.month, now.day).isocalendar()[1] - 1
    return week, now.year
