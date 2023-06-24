"""add foreign-key to posts table

Revision ID: 3f4963f5cc02
Revises: c2d0b29a0f67
Create Date: 2023-06-24 20:40:52.524247

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f4963f5cc02'
down_revision = 'c2d0b29a0f67'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('owner_id', sa.Integer, sa.ForeignKey(
                      "users.id", ondelete='CASCADE'), nullable=False)
                  )


def downgrade() -> None:
    op.drop_column('posts', 'owner_id')
