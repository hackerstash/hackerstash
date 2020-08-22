from hackerstash.db import db
from hackerstash.utils.contest import get_week_and_year


class Challenge(db.Model):
    __tablename__ = 'challenges'

    id = db.Column(db.Integer, primary_key=True)

    key = db.Column(db.String)

    year = db.Column(db.Integer)
    week = db.Column(db.Integer)

    count = db.Column(db.Integer, nullable=False)

    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self) -> str:
        return f'<Challenge {self.id}>'

    def inc(self):
        max_count = Challenge.get_max_count_for(self.key)
        if not self.count >= max_count:
            self.count += 1

    @classmethod
    def get_max_count_for(cls, key: str) -> int:
        if key in ['published_a_post', 'comment_on_a_competitors_post', 'award_two_hundred_points']:
            return 1
        if key in ['award_points_to_three_projects', 'award_points_to_three_posts']:
            return 3
        if key in ['comment_on_five_competitors_posts', 'earn_twenty_five_points_for_one_post', 'have_five_comments_upvoted', 'five_day_post_streak', 'earn_twenty_five_points_for_three_seperate_posts']:
            return 5
        if key in ['award_points_to_ten_projects', 'award_points_to_ten_posts']:
            return 10
        raise Exception('Not sure what the max should be?! %s', key)

    @classmethod
    def find_or_create(cls, project, key: str):
        week, year = get_week_and_year()
        exists = next((x for x in project.challenges if x.key == key and x.week == week), None)

        if exists:
            return exists
        else:
            challenge = Challenge(
                key=key,
                year=year,
                week=week,
                count=0,
                project=project
            )
            db.session.add(challenge)
            db.session.commit()
            return challenge
