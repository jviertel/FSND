"""empty message

Revision ID: 1c90323a3383
Revises: c3e29125fa28
Create Date: 2020-12-11 14:36:38.095957

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c90323a3383'
down_revision = 'c3e29125fa28'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('start_time', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Show', 'start_time')
    # ### end Alembic commands ###
