"""Add columns to Url

Revision ID: 422804c08a20
Revises: 
Create Date: 2016-04-02 11:39:13.097323

"""

# revision identifiers, used by Alembic.
revision = '422804c08a20'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

import datetime


def upgrade():
    op.add_column('urls', sa.Column('created_at', sa.DateTime, default=datetime.datetime.utcnow))
    op.add_column('urls', sa.Column('modified_at', sa.DateTime, default=datetime.datetime.utcnow))


def downgrade():
    op.drop_column('urls', 'created_at')
    op.drop_column('urls', 'modified_at')
