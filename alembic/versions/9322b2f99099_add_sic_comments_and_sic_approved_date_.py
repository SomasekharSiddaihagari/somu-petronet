"""add sic comments and sic approved date to moc_request_history

Revision ID: 9322b2f99099
Revises: 28d6c4641a89
Create Date: 2026-01-14 16:51:52.825151

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9322b2f99099'
down_revision: Union[str, Sequence[str], None] = '28d6c4641a89'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "moc_request_history",
        sa.Column("sic_comments", sa.Text(), nullable=True)
    )
    op.add_column(
        "moc_request_history",
        sa.Column("sic_approved_date", sa.DateTime(), nullable=True)
    )


def downgrade():
    op.drop_column("moc_request_history", "sic_approved_date")
    op.drop_column("moc_request_history", "sic_comments")