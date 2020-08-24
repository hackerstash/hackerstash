challenge_types = [
    'published_a_post',
    'comment_on_a_competitors_post',
    'award_points_to_three_projects',
    'award_points_to_three_posts',
    'award_points_to_ten_projects',
    'award_points_to_ten_posts',
    'comment_on_five_competitors_posts',
    'five_day_post_streak',
    'earn_twenty_five_points_for_one_post',
    'have_five_comments_upvoted',
    'earn_twenty_five_points_for_three_seperate_posts',
    'award_two_hundred_points'
]


def get_score_for_key(key: str) -> int:
    if key in [
        'award_points_to_ten_projects'
    ]:
        return 35
    if key in [
        'award_two_hundred_points'
    ]:
        return 25
    if key in [
        'five_day_post_streak',
        'comment_on_five_competitors_posts',
        'award_points_to_ten_posts'
    ]:
        return 20
    if key in [
        'earn_twenty_five_points_for_three_seperate_posts',
        'have_five_comments_upvoted',
        'award_points_to_three_projects'
    ]:
        return 15
    if key in [
        'published_a_post',
        'earn_twenty_five_points_for_one_post'
    ]:
        return 10
    if key in [
        'award_points_to_three_posts'
    ]:
        return 9
    if key in [
        'comment_on_a_competitors_post'
    ]:
        return 5


def get_max_count_for_key(key: str) -> int:
    if key in [
        'published_a_post',
        'comment_on_a_competitors_post',
        'award_two_hundred_points'
    ]:
        return 1
    if key in [
        'award_points_to_three_projects',
        'award_points_to_three_posts'
    ]:
        return 3
    if key in [
        'comment_on_five_competitors_posts',
        'earn_twenty_five_points_for_one_post',
        'have_five_comments_upvoted',
        'five_day_post_streak',
        'earn_twenty_five_points_for_three_seperate_posts'
    ]:
        return 5
    if key in [
        'award_points_to_ten_projects',
        'award_points_to_ten_posts'
    ]:
        return 10
    raise Exception('Not sure what the max should be?! %s', key)
