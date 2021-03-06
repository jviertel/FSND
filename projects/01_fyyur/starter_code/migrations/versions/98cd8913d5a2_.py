"""empty message

Revision ID: 98cd8913d5a2
Revises: e0e40b71d8bc
Create Date: 2020-12-09 16:43:19.775019

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98cd8913d5a2'
down_revision = 'e0e40b71d8bc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Show',
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['Venue.id'], ),
    sa.PrimaryKeyConstraint('venue_id', 'artist_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Show')
    # ### end Alembic commands ###
