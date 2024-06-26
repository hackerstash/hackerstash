"""Initial migration

Revision ID: 1c9d184e53d0
Revises: 
Create Date: 2020-11-13 21:30:03.322862

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c9d184e53d0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'projects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('url', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('avatar', sa.String(), nullable=True),
        sa.Column('banner', sa.String(), nullable=True),
        sa.Column('location', sa.String(), nullable=True),
        sa.Column('start_month', sa.Integer(), nullable=True),
        sa.Column('start_year', sa.Integer(), nullable=True),
        sa.Column('time_commitment', sa.String(), nullable=True),
        sa.Column('team_size', sa.Integer(), nullable=True),
        sa.Column('profile_button', sa.JSON(none_as_null=True), nullable=True),
        sa.Column('looking_for_cofounders', sa.Boolean(), nullable=True),
        sa.Column('business_models', sa.ARRAY(sa.String()), nullable=True),
        sa.Column('fundings', sa.ARRAY(sa.String()), nullable=True),
        sa.Column('platforms_and_devices', sa.ARRAY(sa.String()), nullable=True),
        sa.Column('ghost', sa.Boolean(), nullable=True),
        sa.Column('published', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'tags',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('icon', sa.String(), nullable=True),
        sa.Column('icon_color', sa.String(), nullable=True),
        sa.Column('background_color', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.String(), nullable=True),
        sa.Column('last_name', sa.String(), nullable=True),
        sa.Column('username', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('admin', sa.Boolean(), nullable=True),
        sa.Column('bio', sa.String(), nullable=True),
        sa.Column('location', sa.String(), nullable=True),
        sa.Column('provider', sa.String(), nullable=True),
        sa.Column('telephone', sa.String(), nullable=True),
        sa.Column('twitter', sa.String(), nullable=True),
        sa.Column('avatar', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )
    op.create_table(
        'challenges',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('key', sa.String(), nullable=True),
        sa.Column('count', sa.Integer(), nullable=False),
        sa.Column('max', sa.Integer(), nullable=False),
        sa.Column('score', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'invites',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('first_name', sa.String(), nullable=True),
        sa.Column('link', sa.String(), nullable=True),
        sa.Column('role', sa.String(), nullable=True),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_table(
        'members',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('owner', sa.Boolean(), nullable=True),
        sa.Column('role', sa.String(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'notifications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(), nullable=True),
        sa.Column('read', sa.Boolean(), nullable=True),
        sa.Column('read_at', sa.DateTime(), nullable=True),
        sa.Column('message', sa.String(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'notifications_settings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('a_follower_posts_an_update_web', sa.Boolean(), nullable=True),
        sa.Column('a_follower_posts_an_update_email', sa.Boolean(), nullable=True),
        sa.Column('a_team_member_joined_your_project_web', sa.Boolean(), nullable=True),
        sa.Column('a_team_member_joined_your_project_email', sa.Boolean(), nullable=True),
        sa.Column('a_team_member_left_your_project_web', sa.Boolean(), nullable=True),
        sa.Column('a_team_member_left_your_project_email', sa.Boolean(), nullable=True),
        sa.Column('someone_comments_on_your_post_web', sa.Boolean(), nullable=True),
        sa.Column('someone_comments_on_your_post_email', sa.Boolean(), nullable=True),
        sa.Column('someone_downvotes_your_comment_web', sa.Boolean(), nullable=True),
        sa.Column('someone_downvotes_your_comment_email', sa.Boolean(), nullable=True),
        sa.Column('someone_downvotes_your_post_web', sa.Boolean(), nullable=True),
        sa.Column('someone_downvotes_your_post_email', sa.Boolean(), nullable=True),
        sa.Column('someone_mentions_you_in_post_or_comment_web', sa.Boolean(), nullable=True),
        sa.Column('someone_mentions_you_in_post_or_comment_email', sa.Boolean(), nullable=True),
        sa.Column('someone_replies_to_your_comment_web', sa.Boolean(), nullable=True),
        sa.Column('someone_replies_to_your_comment_email', sa.Boolean(), nullable=True),
        sa.Column('someone_upvotes_your_comment_web', sa.Boolean(), nullable=True),
        sa.Column('someone_upvotes_your_comment_email', sa.Boolean(), nullable=True),
        sa.Column('someone_upvotes_your_post_web', sa.Boolean(), nullable=True),
        sa.Column('someone_upvotes_your_post_email', sa.Boolean(), nullable=True),
        sa.Column('you_have_a_new_follower_web', sa.Boolean(), nullable=True),
        sa.Column('you_have_a_new_follower_email', sa.Boolean(), nullable=True),
        sa.Column('you_were_invited_to_join_a_project_web', sa.Boolean(), nullable=True),
        sa.Column('you_were_invited_to_join_a_project_email', sa.Boolean(), nullable=True),
        sa.Column('you_were_removed_from_a_project_web', sa.Boolean(), nullable=True),
        sa.Column('you_were_removed_from_a_project_email', sa.Boolean(), nullable=True),
        sa.Column('project_vote_reminder_web', sa.Boolean(), nullable=True),
        sa.Column('project_vote_reminder_email', sa.Boolean(), nullable=True),
        sa.Column('prize_awarded_web', sa.Boolean(), nullable=True),
        sa.Column('prize_awarded_email', sa.Boolean(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('body', sa.String(), nullable=False),
        sa.Column('url_slug', sa.String(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('tag_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'reviews',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('url', sa.String(), nullable=True),
        sa.Column('thumbnail', sa.String(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'users_following',
        sa.Column('follower_id', sa.Integer(), nullable=True),
        sa.Column('followed_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['followed_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['follower_id'], ['users.id'], )
    )
    op.create_table(
        'users_groups',
        sa.Column('tag_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('tag_id', 'user_id')
    )
    op.create_table(
        'winners',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('position', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'comments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('body', sa.String(), nullable=True),
        sa.Column('parent_comment_id', sa.Integer(), nullable=True),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'polls',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('question', sa.String(), nullable=False),
        sa.Column('choices', sa.JSON(none_as_null=True), nullable=True),
        sa.Column('post_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'votes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(), nullable=True),
        sa.Column('score', sa.Integer(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=True),
        sa.Column('post_id', sa.Integer(), nullable=True),
        sa.Column('comment_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['comment_id'], ['comments.id'], ),
        sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('votes')
    op.drop_table('polls')
    op.drop_table('comments')
    op.drop_table('winners')
    op.drop_table('users_groups')
    op.drop_table('users_following')
    op.drop_table('reviews')
    op.drop_table('posts')
    op.drop_table('notifications_settings')
    op.drop_table('notifications')
    op.drop_table('members')
    op.drop_table('invites')
    op.drop_table('challenges')
    op.drop_table('users')
    op.drop_table('tags')
    op.drop_table('projects')
    # ### end Alembic commands ###
