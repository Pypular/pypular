"""Add expanded_url column to Url

Revision ID: f7caee030cf5
Revises: 422804c08a20
Create Date: 2016-04-02 14:09:14.343936

"""

# revision identifiers, used by Alembic.
revision = 'f7caee030cf5'
down_revision = '422804c08a20'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('urls', sa.Column('expanded_url', sa.Text, unique=True))


def downgrade():
    op.drop_column('urls', 'expanded_url')
