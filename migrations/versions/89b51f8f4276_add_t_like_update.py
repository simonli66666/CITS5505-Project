"""add t_like update

Revision ID: 89b51f8f4276
Revises: b96cd8aa4e17
Create Date: 2024-05-13 19:51:44.319889

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89b51f8f4276'
down_revision = 'b96cd8aa4e17'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('t_like',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('post_id', sa.INTEGER(), nullable=True),
    sa.Column('timestamps', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['t_post.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['t_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('likes')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('likes',
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('post_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['t_post.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['t_user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    op.drop_table('t_like')
    # ### end Alembic commands ###
