import datetime


def get_contest_name():
    now = datetime.datetime.now()
    week = datetime.date(now.year, now.month, now.day).isocalendar()[1]

    return f'contest_{str(week)}_{str(now.year)}'
