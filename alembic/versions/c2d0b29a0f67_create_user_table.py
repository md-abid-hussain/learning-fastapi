"""create user table

Revision ID: c2d0b29a0f67
Revises: 516a2fafc4cd
Create Date: 2023-06-24 19:31:45.710312

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2d0b29a0f67'
down_revision = '516a2fafc4cd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer, nullable=False,
                              primary_key=True),
                    sa.Column('email', sa.String, unique=True, nullable=False),
                    sa.Column('password', sa.String, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP,
                              server_default=sa.text('now()'), nullable=False)
                    )


def downgrade() -> None:
    op.drop_table('users')
