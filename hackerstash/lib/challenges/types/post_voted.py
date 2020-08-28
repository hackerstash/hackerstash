from flask import g
from hackerstash.lib.challenges.base import Base
from hackerstash.lib.logging import logging
from hackerstash.utils.contest import get_week_and_year


def is_not_members_post(user, post):
    return user.member.project.id != post.project.id


class PostVoted(Base):
    def __init__(self, payload: dict) -> None:
        super().__init__(payload)

        user = g.user
        post = payload['post']

        if is_not_members_post(user, post):
            if not self.has_completed(user.member.project, 'award_points_to_three_posts'):
                logging.info(f'Awarding \'award_points_to_three_posts\' challenge for \'{user.member.project.name}\'')
                user.member.project.create_or_inc_challenge('award_points_to_three_posts')

            if not self.has_completed(user.member.project, 'award_points_to_ten_posts'):
                logging.info(f'Awarding \'award_points_to_ten_posts\' challenge for \'{user.member.project.name}\'')
                user.member.project.create_or_inc_challenge('award_points_to_ten_posts')

            if not self.has_completed(post.project, 'earn_twenty_five_points_for_one_post'):
                logging.info(f'Awarding \'earn_twenty_five_points_for_one_post\' challenge for \'{post.project.name}\'')
                post.project.create_or_inc_challenge('earn_twenty_five_points_for_one_post')

            if not self.has_completed(post.project, 'earn_twenty_five_points_for_three_seperate_posts'):
                week, year = get_week_and_year()
                posts_this_week = list(filter(lambda x: x.week == week and x.year == year, post.project.posts))
                count = 0

                for p in posts_this_week:
                    if p.vote_score >= 25:
                        count += 1

                print(count)

                # Can't be any higher than 3
                logging.info(f'Setting \'earn_twenty_five_points_for_three_seperate_posts\' challenge for \'{post.project.name}\' to \'{count}\'')
                post.project.create_or_set_challenge('earn_twenty_five_points_for_three_seperate_posts', count)
