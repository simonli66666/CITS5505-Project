"""add t_like update

Revision ID: b96cd8aa4e17
Revises: 9d44793e7a79
Create Date: 2024-05-13 19:45:23.242460

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b96cd8aa4e17'
down_revision = '9d44793e7a79'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('t_like')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('t_like',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('post_id', sa.INTEGER(), nullable=True),
    sa.Column('timestamps', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['t_post.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['t_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
