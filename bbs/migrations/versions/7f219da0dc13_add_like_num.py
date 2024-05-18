"""Add like_num

Revision ID: 7f219da0dc13
Revises: 3a1e1459b979
Create Date: 2024-05-12 16:00:14.955144

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f219da0dc13'
down_revision = '3a1e1459b979'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('t_user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('badges', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('like_num', sa.INTEGER(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('t_user', schema=None) as batch_op:
        batch_op.drop_column('like_num')
        batch_op.drop_column('badges')

    # ### end Alembic commands ###