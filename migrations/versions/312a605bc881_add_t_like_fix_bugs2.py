"""add t_like fix bugs2

Revision ID: 312a605bc881
Revises: 8bca7da29c4b
Create Date: 2024-05-13 19:00:33.388593

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '312a605bc881'
down_revision = '8bca7da29c4b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('t_post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('likes_num', sa.INTEGER(), nullable=True, comment='like post persons'))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('t_post', schema=None) as batch_op:
        batch_op.drop_column('likes_num')

    # ### end Alembic commands ###
