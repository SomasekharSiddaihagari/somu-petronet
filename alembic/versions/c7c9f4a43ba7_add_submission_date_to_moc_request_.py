"""add submission_date to moc_request_history

Revision ID: c7c9f4a43ba7
Revises: 9322b2f99099
Create Date: 2026-01-14 16:55:55.967929

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c7c9f4a43ba7'
down_revision: Union[str, Sequence[str], None] = '9322b2f99099'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.add_column(
        "moc_request_history",
        sa.Column("submission_date", sa.DateTime(), nullable=True)
    )


def downgrade():
    op.drop_column("moc_request_history", "submission_date")