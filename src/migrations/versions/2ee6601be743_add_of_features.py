"""add of features

Revision ID: 2ee6601be743
Revises: 4ad96c316f26
Create Date: 2022-05-07 14:48:14.139519

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ee6601be743'
down_revision = '4ad96c316f26'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('is_offer_of_the_day', sa.Boolean(), nullable=False))
    op.add_column('products', sa.Column('is_popular', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'is_popular')
    op.drop_column('products', 'is_offer_of_the_day')
    # ### end Alembic commands ###
