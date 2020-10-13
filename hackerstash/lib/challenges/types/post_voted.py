from flask import g
from hackerstash.lib.challenges.base import Base
from hackerstash.lib.logging import Logging
from hackerstash.utils.contest import get_week_and_year

log = Logging(module='Challenges::PostVoted')


def is_not_members_post(user, post):
    return user.member.project.id != post.project.id


class PostVoted(Base):
    def __init__(self, payload: dict) -> None:
        super().__init__(payload)

        user = g.user
        post = payload['post']

        if is_not_members_post(user, post):
            if not self.has_completed(user.member.project, 'award_points_to_three_posts'):
                log.info('Incrementing challenge', {'type': 'award_points_to_three_posts', 'project_id': user.member.project.id})
                user.member.project.create_or_inc_challenge('award_points_to_three_posts')

            if not self.has_completed(post.project, 'earn_twenty_five_points_for_one_post'):
                all_posts = post.project.posts
                for p in all_posts:
                    # The 25 points have to all be from this current contest
                    votes_this_week = list(filter(lambda x: x.is_current_contest, p.votes))
                    this_week_score = sum(vote.score for vote in votes_this_week)
                    if this_week_score >= 25:
                        log.info('Incrementing challenge', {'type': 'earn_twenty_five_points_for_one_post', 'project_id': post.project.id})
                        post.project.create_or_inc_challenge('earn_twenty_five_points_for_one_post')

            if not self.has_completed(post.project, 'earn_twenty_five_points_for_three_seperate_posts'):
                week, year = get_week_and_year()
                posts_this_week = list(filter(lambda x: x.week == week and x.year == year, post.project.posts))
                count = 0

                for p in posts_this_week:
                    if p.vote_score >= 25:
                        count += 1

                # Can't be any higher than 3
                log.info('Incrementing challenge', {'type': 'earn_twenty_five_points_for_three_seperate_posts', 'project_id': post.project.id})
                post.project.create_or_set_challenge('earn_twenty_five_points_for_three_seperate_posts', count)
