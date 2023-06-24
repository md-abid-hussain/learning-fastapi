"""adding remaining column in the post table

Revision ID: 49ae64394d9a
Revises: 3f4963f5cc02
Create Date: 2023-06-24 20:54:37.542630

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49ae64394d9a'
down_revision = '3f4963f5cc02'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean,
                  nullable=False, server_default=sa.text('False')))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(
        timezone=True), nullable=False, server_default=sa.text('now()')))


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
