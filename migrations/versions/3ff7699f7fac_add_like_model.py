"""Add Like model

Revision ID: 3ff7699f7fac
Revises: 3b0247a692b6
Create Date: 2025-07-24 18:34:00.665432
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '3ff7699f7fac'
down_revision = '6b773d69f384'  # or whatever your last valid migration is
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('likes',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('post_id', sa.Integer(), sa.ForeignKey('posts.id'), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=False, server_default=sa.func.now())
    )

def downgrade():
    op.drop_table('likes')