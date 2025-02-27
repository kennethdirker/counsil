"""add state field to Discussion model

Revision ID: c6a229700313
Revises: 52e4e9957801
Create Date: 2025-01-06 17:12:55.026394

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6a229700313'
down_revision = '52e4e9957801'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('discussion', schema=None) as batch_op:
        batch_op.add_column(sa.Column('state', sa.String(length=256), server_default='SETUP', nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('discussion', schema=None) as batch_op:
        batch_op.drop_column('state')

    # ### end Alembic commands ###
