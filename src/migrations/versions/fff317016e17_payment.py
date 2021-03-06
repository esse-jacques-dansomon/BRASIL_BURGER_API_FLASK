"""payment

Revision ID: fff317016e17
Revises: b41aaed43620
Create Date: 2022-04-25 14:13:13.579833

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'fff317016e17'
down_revision = 'b41aaed43620'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('images_ibfk_1', 'images', type_='foreignkey')
    op.create_foreign_key(None, 'images', 'products', ['product_id'], ['id'], ondelete='CASCADE')
    op.add_column('payments', sa.Column('paid_at', sa.DateTime(), nullable=True))
    op.add_column('payments', sa.Column('is_paid', sa.Boolean(), nullable=True))
    op.drop_column('payments', 'date')
    op.drop_column('payments', 'amount')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('payments', sa.Column('amount', mysql.FLOAT(), nullable=True))
    op.add_column('payments', sa.Column('date', mysql.DATETIME(), nullable=True))
    op.drop_column('payments', 'is_paid')
    op.drop_column('payments', 'paid_at')
    op.drop_constraint(None, 'images', type_='foreignkey')
    op.create_foreign_key('images_ibfk_1', 'images', 'products', ['product_id'], ['id'])
    # ### end Alembic commands ###
