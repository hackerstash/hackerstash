from hackerstash.db import db


class NotificationSetting(db.Model):
    __tablename__ = 'notifications_settings'

    id = db.Column(db.Integer, primary_key=True)

    a_follower_posts_an_update_web = db.Column(db.Boolean, default=True)
    a_follower_posts_an_update_email = db.Column(db.Boolean, default=True)

    a_team_member_joined_your_project_web = db.Column(db.Boolean, default=True)
    a_team_member_joined_your_project_email = db.Column(db.Boolean, default=True)

    a_team_member_left_your_project_web = db.Column(db.Boolean, default=True)
    a_team_member_left_your_project_email = db.Column(db.Boolean, default=True)

    someone_comments_on_your_post_web = db.Column(db.Boolean, default=True)
    someone_comments_on_your_post_email = db.Column(db.Boolean, default=True)

    someone_downvotes_your_comment_web = db.Column(db.Boolean, default=True)
    someone_downvotes_your_comment_email = db.Column(db.Boolean, default=False)

    someone_downvotes_your_post_web = db.Column(db.Boolean, default=True)
    someone_downvotes_your_post_email = db.Column(db.Boolean, default=False)

    someone_mentions_you_in_post_or_comment_web = db.Column(db.Boolean, default=True)
    someone_mentions_you_in_post_or_comment_email = db.Column(db.Boolean, default=True)

    someone_replies_to_your_comment_web = db.Column(db.Boolean, default=True)
    someone_replies_to_your_comment_email = db.Column(db.Boolean, default=True)

    someone_upvotes_your_comment_web = db.Column(db.Boolean, default=True)
    someone_upvotes_your_comment_email = db.Column(db.Boolean, default=False)

    someone_upvotes_your_post_web = db.Column(db.Boolean, default=True)
    someone_upvotes_your_post_email = db.Column(db.Boolean, default=True)

    you_have_a_new_follower_web = db.Column(db.Boolean, default=True)
    you_have_a_new_follower_email = db.Column(db.Boolean, default=True)

    you_were_invited_to_join_a_project_web = db.Column(db.Boolean, default=True)
    you_were_invited_to_join_a_project_email = db.Column(db.Boolean, default=True)

    you_were_removed_from_a_project_web = db.Column(db.Boolean, default=True)
    you_were_removed_from_a_project_email = db.Column(db.Boolean, default=True)

    project_vote_reminder_web = db.Column(db.Boolean, default=True)
    project_vote_reminder_email = db.Column(db.Boolean, default=True)

    prize_awarded_web = db.Column(db.Boolean, default=True)
    prize_awarded_email = db.Column(db.Boolean, default=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self) -> str:
        return f'<NotificationSetting {self.user.id}>'
