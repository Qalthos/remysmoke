"""Add Unsmoke

Revision ID: 296f735b773b
Revises: None
Create Date: 2013-07-21 18:14:07.679454

"""

# revision identifiers, used by Alembic.
revision = '296f735b773b'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'unsmoke',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('date', sa.Date, nullable=False),
        sa.Column('user', sa.Unicode(255), nullable=False),
    )


def downgrade():
    op.drop_table('unsmoke')
