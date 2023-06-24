"""add content column in posts table

Revision ID: 516a2fafc4cd
Revises: 7b15f2129c19
Create Date: 2023-06-24 19:23:11.092162

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '516a2fafc4cd'
down_revision = '7b15f2129c19'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('content', sa.String, nullable=False)
                  )


def downgrade() -> None:
    op.drop_column('posts', 'content')
