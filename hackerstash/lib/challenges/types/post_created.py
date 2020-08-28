from flask import g
from hackerstash.lib.challenges.base import Base
from hackerstash.lib.logging import logging
from hackerstash.utils.contest import get_week_and_year
from hackerstash.utils.helpers import find_in_list


class PostCreated(Base):
    def __init__(self, payload: dict) -> None:
        super().__init__(payload)

        project = g.user.member.project

        if not self.has_completed(project, 'published_a_post'):
            logging.info(f'Awarding \'published_a_post\' challenge for \'{project.name}\'')
            project.create_or_inc_challenge('published_a_post')

        # This is a bit of weird one as they can actually
        # regress. Ideally we would check this on a cron
        # or something so it's always up to date.
        if not self.has_completed(project, 'five_day_post_streak'):
            week, year = get_week_and_year()
            posts_this_week = list(filter(lambda x: x.week == week and x.year == year, project.posts))
            streak = 0

            for i in range(6):
                # If they've already hit the challenge we should skip the check.
                # Otherwise they could get mon-fri, but we will reset to 0 on sat.
                if streak < 5:
                    match = find_in_list(posts_this_week, lambda x: x.day == i + 1)
                    if match:
                        streak += 1
                    else:
                        streak = 0

            logging.info(f'Setting \'five_day_post_streak\' challenge for \'{project.name}\' to \'{streak}\'')
            project.create_or_set_challenge('five_day_post_streak', streak)
