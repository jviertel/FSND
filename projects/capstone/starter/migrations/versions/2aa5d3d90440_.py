"""empty message

Revision ID: 2aa5d3d90440
Revises: 1751147036cb
Create Date: 2021-01-22 18:38:27.701048

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2aa5d3d90440'
down_revision = '1751147036cb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Manufacturer', 'image_link')
    op.drop_column('Manufacturer', 'fb_link')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Manufacturer', sa.Column('fb_link', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    op.add_column('Manufacturer', sa.Column('image_link', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    # ### end Alembic commands ###