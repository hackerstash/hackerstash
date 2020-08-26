"""Remove week and year from challenge

Revision ID: 6a69eacae770
Revises: d48c59b21dbb
Create Date: 2020-08-24 14:01:26.593710

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a69eacae770'
down_revision = 'd48c59b21dbb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('challenges', 'week')
    op.drop_column('challenges', 'year')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('challenges', sa.Column('year', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('challenges', sa.Column('week', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###