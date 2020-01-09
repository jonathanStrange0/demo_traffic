"""fixed relationship between integration platform and url

Revision ID: 5056cf879a3e
Revises: 8d35b7d2013d
Create Date: 2020-01-09 05:33:00.198161

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5056cf879a3e'
down_revision = '8d35b7d2013d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('url', sa.Column('platform_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'url', 'integration_platform', ['platform_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'url', type_='foreignkey')
    op.drop_column('url', 'platform_id')
    # ### end Alembic commands ###