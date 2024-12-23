"""posts table

Revision ID: 35b6ec25a6cd
Revises: 32c6391a77e5
Create Date: 2024-12-09 19:54:07.649019

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35b6ec25a6cd'
down_revision = '32c6391a77e5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('discussion_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['discussion_id'], ['discussion.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_post_created_at'), ['created_at'], unique=False)
        batch_op.create_index(batch_op.f('ix_post_discussion_id'), ['discussion_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_post_user_id'), ['user_id'], unique=False)

    with op.batch_alter_table('discussion', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=False))
        batch_op.create_index(batch_op.f('ix_discussion_created_at'), ['created_at'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('discussion', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_discussion_created_at'))
        batch_op.drop_column('created_at')

    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_post_user_id'))
        batch_op.drop_index(batch_op.f('ix_post_discussion_id'))
        batch_op.drop_index(batch_op.f('ix_post_created_at'))

    op.drop_table('post')
    # ### end Alembic commands ###
