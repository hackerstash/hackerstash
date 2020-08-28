from flask import session
from hackerstash.lib.logging import logging

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


def mark_as_complete(challenge):
    logging.info(f'Challenge "{challenge.key}" has been completed by "{challenge.project.name}", let the confetti commence!')
    session['challenge_completed'] = get_completed_message_for_challenge(challenge)


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
        'award_points_to_three_posts',
        'earn_twenty_five_points_for_three_seperate_posts'
    ]:
        return 3
    if key in [
        'comment_on_five_competitors_posts',
        'earn_twenty_five_points_for_one_post',
        'have_five_comments_upvoted',
        'five_day_post_streak'
    ]:
        return 5
    if key in [
        'award_points_to_ten_projects',
        'award_points_to_ten_posts'
    ]:
        return 10
    raise Exception('Not sure what the max should be?! %s', key)


def get_completed_message_for_challenge(challenge) -> str:
    key = challenge.key
    points = get_score_for_key(key)
    if key == 'published_a_post':
        return f'You earned <span>{points} points</span> for your project by publishing your first post of the week ⛅️'
    if key == 'comment_on_a_competitors_post':
        return f'You earned <span>{points} points</span> for your project by commenting on a competitor’s post 💬'
    if key == 'award_points_to_three_projects':
        return f'You earned <span>{points} points</span> for your project by awarding points to 3 of your competitor’s projects 💪'
    if key == 'award_points_to_three_posts':
        return f'You earned <span>{points} points</span> for your project by awarding points to 3 of your competitor’s posts 😍'
    if key == 'award_points_to_ten_projects':
        return f'You earned <span>{points} points</span> for your project by awarding points to 10 of your competitor’s projects 💪'
    if key == 'award_points_to_ten_posts':
        return f'You earned <span>{points} points</span> for your project by awarding points to 3 of your competitor’s posts 😍'
    if key == 'comment_on_five_competitors_posts':
        return f'You earned <span>{points} points</span> for your project by commenting on 5 of your competitor’s posts 💬'
    if key == 'five_day_post_streak':
        return f'You earned <span>{points} points</span> for your project by publishing at least 1 new {challenge.project.name} post a day for 5 days 🙌'
    if key == 'earn_twenty_five_points_for_one_post':
        return f'You earned <span>{points} points</span> for your project because one of your posts earned 25 points from your competitors 😊'
    if key == 'have_five_comments_upvoted':
        return f'You earned <span>{points} points</span> for your project by by having 5 of your comments upvoted by competitors 💑'
    if key == 'earn_twenty_five_points_for_three_seperate_posts':
        return f'You earned <span>{points} points</span> for your project because 3 of your posts earned at least 25 points each from your competitors 💥'
    if key == 'award_two_hundred_points':
        return f'You earned <span>{points} points</span> for your project by awarding 200 points to competing projects 😇'
    raise Exception(f'Cound not find a message for {key}')
