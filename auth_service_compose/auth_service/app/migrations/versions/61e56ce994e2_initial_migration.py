"""Initial migration.

Revision ID: 61e56ce994e2
Revises: 
Create Date: 2022-07-16 22:29:28.660633

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61e56ce994e2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'logs', ['id'])
    op.create_unique_constraint(None, 'refresh_tokens', ['id'])
    op.create_unique_constraint(None, 'roles', ['id'])
    op.create_unique_constraint(None, 'users', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'roles', type_='unique')
    op.drop_constraint(None, 'refresh_tokens', type_='unique')
    op.drop_constraint(None, 'logs', type_='unique')
    # ### end Alembic commands ###
