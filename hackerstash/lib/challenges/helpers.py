from hackerstash.lib.logging import Logging
from hackerstash.lib.redis import redis

log = Logging(module='Challenges')

challenge_types = [
    'published_a_post',
    'comment_on_a_competitors_post',
    'award_points_to_three_posts',
    'award_ponts_to_three_projects',
    'comment_on_five_competitors_posts',
    'earn_twenty_five_points_for_one_post',
    'have_five_comments_upvoted',
    'earn_twenty_five_points_for_three_seperate_posts'
]


def mark_as_complete(challenge):
    log.info('Challenge completed', {'challenge_id': challenge.id})
    message = get_completed_message_for_challenge(challenge)
    redis.set(f'{challenge.project.id}:challenge_completed', message)


def get_score_for_key(key: str) -> int:
    if key in ['comment_on_five_competitors_posts']:
        return 20
    if key in ['earn_twenty_five_points_for_three_seperate_posts', 'have_five_comments_upvoted', 'award_ponts_to_three_projects']:
        return 15
    if key in ['published_a_post', 'earn_twenty_five_points_for_one_post']:
        return 10
    if key in ['award_points_to_three_posts']:
        return 9
    if key in ['comment_on_a_competitors_post']:
        return 5


def get_max_count_for_key(key: str) -> int:
    if key in ['published_a_post', 'comment_on_a_competitors_post', 'earn_twenty_five_points_for_one_post']:
        return 1
    if key in ['award_points_to_three_posts', 'earn_twenty_five_points_for_three_seperate_posts', 'award_ponts_to_three_projects']:
        return 3
    if key in ['comment_on_five_competitors_posts', 'have_five_comments_upvoted']:
        return 5
    raise Exception('Not sure what the max should be?! %s', key)


def get_completed_message_for_challenge(challenge) -> str:
    key = challenge.key
    points = get_score_for_key(key)
    if key == 'published_a_post':
        return f'You earned <span>{points} points</span> for your project by publishing your first post of the week ⛅️'
    if key == 'comment_on_a_competitors_post':
        return f'You earned <span>{points} points</span> for your project by commenting on a competitor’s post 💬'
    if key == 'award_points_to_three_posts':
        return f'You earned <span>{points} points</span> for your project by awarding points to 3 of your competitor’s posts 😍'
    if key == 'award_ponts_to_three_projects':
        return f'You earned <span>{points} points</span> for your project by awarding points to 3 of your competitor’s projects 👌'
    if key == 'comment_on_five_competitors_posts':
        return f'You earned <span>{points} points</span> for your project by commenting on 5 of your competitor’s posts 💬'
    if key == 'earn_twenty_five_points_for_one_post':
        return f'You earned <span>{points} points</span> for your project because one of your posts earned 25 points from your competitors 😊'
    if key == 'have_five_comments_upvoted':
        return f'You earned <span>{points} points</span> for your project by by having 5 of your comments upvoted by competitors 💑'
    if key == 'earn_twenty_five_points_for_three_seperate_posts':
        return f'You earned <span>{points} points</span> for your project because 3 of your posts earned at least 25 points each from your competitors 💥'
    raise Exception(f'Cound not find a message for {key}')
