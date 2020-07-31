from datetime import datetime
from hackerstash.models.project import Project


def sidebar_data():
    now = datetime.now()
    count = Project.query.count() * 10
    prize_pool = f'${count}.00'
    remaining_days = f'{6 - now.weekday()} days'

    return prize_pool, remaining_days
