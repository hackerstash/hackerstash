import datetime
from hackerstash.models.challenge import Challenge


class ChallengeCount:
    def __init__(self, challenge_list):
        self.challenge_list = challenge_list

    def get_count_by_key(self, key: str) -> int:
        challenge = next((x for x in self.challenge_list if x.key == key and x.week == self.week), None)
        return challenge.count if challenge else 0

    def has_completed(self, key: str) -> bool:
        count = self.get_count_by_key(key)
        max_count = Challenge.get_max_count_for(key)
        return max_count <= count

    def get_multiplier_for_key(self, key: str) -> int:
        # TODO:
        # award_points_to_ten_projects, award_points_to_ten_posts and some others
        # are calculated incorrectly as they do x*y, but they don't start from 0.
        if key in ['award_one_hundred_points']:
            return 25
        if key in ['published_a_post']:
            return 10
        if key in ['comment_on_a_competitors_post', 'award_points_to_ten_projects', 'award_points_to_ten_posts']:
            return 5
        if key in ['five_day_post_streak', 'earn_five_points_for_three_seperate_posts', 'comment_on_five_competitors_posts']:
            return 4
        if key in ['award_points_to_three_projects', 'award_points_to_three_posts', 'have_five_comments_upvoted']:
            return 3
        if key in ['earn_five_points_for_one_post']:
            return 2
        raise Exception('Not sure how to multiply %s', key)

    @property
    def week(self):
        now = datetime.datetime.now()
        return datetime.date(now.year, now.month, now.day).isocalendar()[1] - 1

    @property
    def completed_challenges_for_the_week(self):
        return list(filter(lambda x: self.has_completed(x.key), self.challenge_list))

    @property
    def challenge_types(self):
        return [
            'published_a_post',
            'comment_on_a_competitors_post',
            'award_points_to_three_projects',
            'award_points_to_three_posts',
            'award_points_to_ten_projects',
            'award_points_to_ten_posts',
            'comment_on_five_competitors_posts',
            'five_day_post_streak',
            'earn_five_points_for_one_post',
            'have_five_comments_upvoted',
            'earn_five_points_for_three_seperate_posts',
            'award_one_hundred_points'  # TODO
        ]
