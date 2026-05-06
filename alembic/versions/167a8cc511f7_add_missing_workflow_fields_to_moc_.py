"""add missing workflow fields to moc_request_history

Revision ID: 167a8cc511f7
Revises: c7c9f4a43ba7
Create Date: 2026-01-14 17:01:12.465566

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '167a8cc511f7'
down_revision: Union[str, Sequence[str], None] = 'c7c9f4a43ba7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "moc_request_history",
        sa.Column("hira_approved_date", sa.DateTime(), nullable=True)
    )
    op.add_column(
        "moc_request_history",
        sa.Column("approved_date", sa.DateTime(), nullable=True)
    )
    op.add_column(
        "moc_request_history",
        sa.Column("closure_date", sa.DateTime(), nullable=True)
    )
    op.add_column(
        "moc_request_history",
        sa.Column("closure_comments", sa.Text(), nullable=True)
    )


def downgrade():
    op.drop_column("moc_request_history", "closure_comments")
    op.drop_column("moc_request_history", "closure_date")
    op.drop_column("moc_request_history", "approved_date")
    op.drop_column("moc_request_history", "hira_approved_date")