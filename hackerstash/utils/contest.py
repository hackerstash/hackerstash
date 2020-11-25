import datetime


def get_week_and_year() -> [int, int]:
    """
    Get the current calendar week and year
    :return: [int, int]
    """
    now = datetime.datetime.now()
    week = datetime.date(now.year, now.month, now.day).isocalendar()[1]
    return week, now.year
