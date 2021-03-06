"""empty message

Revision ID: 55e2c2f84cc8
Revises: 439a0805fc3c
Create Date: 2020-01-09 09:35:11.937651

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55e2c2f84cc8'
down_revision = '439a0805fc3c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('url', sa.Column('num_headless', sa.Integer(), nullable=True))
    op.add_column('url', sa.Column('num_windows', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('url', 'num_windows')
    op.drop_column('url', 'num_headless')
    # ### end Alembic commands ###
