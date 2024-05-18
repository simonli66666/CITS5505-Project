"""add t_like

Revision ID: 7862a8021759
Revises: ddbfc16e8b57
Create Date: 2024-05-13 18:38:38.313324

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7862a8021759'
down_revision = 'ddbfc16e8b57'
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
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('t_like')
    # ### end Alembic commands ###