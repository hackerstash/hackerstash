"""Add ProgressSetting model

Revision ID: eedcef7b8bf5
Revises: 491d9da368bc
Create Date: 2020-08-15 15:14:23.027409

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eedcef7b8bf5'
down_revision = '491d9da368bc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('progress_settings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('enabled', sa.Boolean(), nullable=True),
    sa.Column('visible', sa.Boolean(), nullable=True),
    sa.Column('columns', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('progress_settings')
    # ### end Alembic commands ###