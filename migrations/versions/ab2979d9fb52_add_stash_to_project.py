"""Add stash to project

Revision ID: ab2979d9fb52
Revises: 3caa8737ef34
Create Date: 2020-09-03 10:11:04.726957

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab2979d9fb52'
down_revision = '3caa8737ef34'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('projects', sa.Column('stash', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('projects', 'stash')
    # ### end Alembic commands ###