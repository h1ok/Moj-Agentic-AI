"""add user profile fields

Revision ID: add_user_profile_fields
Revises: 
Create Date: 2026-01-20

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_user_profile_fields'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('name', sa.String(255), nullable=True))
    op.add_column('users', sa.Column('profile_picture', sa.String(500), nullable=True))


def downgrade():
    op.drop_column('users', 'profile_picture')
    op.drop_column('users', 'name')
