"""initial_migration

Revision ID: 8e5534c2d440
Revises: 
Create Date: 2022-07-28 03:34:33.623622

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8e5534c2d440'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.create_table('roles',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('level', sa.INTEGER(), nullable=False),
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('users',
    sa.Column('login', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('login')
    )
    op.create_table('logs',
    sa.Column('device', sa.String(), nullable=False),
    sa.Column('when', sa.TIMESTAMP(), nullable=False),
    sa.Column('action', sa.Enum('login', 'logout', 'logout_everywhere', 'other', name='actions_enum'), nullable=False),
    sa.Column('method', sa.Enum('post', 'get', 'put', 'delete', 'update', 'patch', name='method_enum'), nullable=False),
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('when', 'id'),
    sa.UniqueConstraint('id', 'when'),
    postgresql_partition_by='range ("when")'
    )
    op.create_table('refresh_tokens',
    sa.Column('token', sa.String(), nullable=False),
    sa.Column('from_', sa.TIMESTAMP(), nullable=False),
    sa.Column('to', sa.TIMESTAMP(), nullable=False),
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('user_roles',
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('role_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_roles')
    op.drop_table('refresh_tokens')
    op.drop_table('logs')
    op.drop_table('users')
    op.drop_table('roles')

    actions_enum = postgresql.ENUM('login', 'logout', 'logout_everywhere', 'other', name='actions_enum')
    actions_enum.drop(op.get_bind())

    method_enum = postgresql.ENUM('post', 'get', 'put', 'delete', 'update', 'patch', name='method_enum')
    method_enum.drop(op.get_bind())
    # ### end Alembic commands ###