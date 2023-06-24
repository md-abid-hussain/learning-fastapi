"""creating post table

Revision ID: 7b15f2129c19
Revises: 
Create Date: 2023-06-24 18:23:56.908827

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b15f2129c19'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',
                    sa.Column('id', sa.Integer, nullable=False,
                              primary_key=True),
                    sa.Column('title', sa.String, nullable=False)
                    )


def downgrade() -> None:
    op.drop_table('posts')
