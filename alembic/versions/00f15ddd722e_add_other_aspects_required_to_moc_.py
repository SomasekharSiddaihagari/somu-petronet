"""add other_aspects_required to moc requests

Revision ID: 00f15ddd722e
Revises: 46a09afe6bbe
Create Date: 2026-02-04 15:55:25.281074

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00f15ddd722e'
down_revision: Union[str, Sequence[str], None] = '46a09afe6bbe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "moc_requests",
        sa.Column("other_aspects_required", sa.Boolean(), nullable=True)
    )

    op.add_column(
        "moc_request_history",
        sa.Column("other_aspects_required", sa.Boolean(), nullable=True)
    )

def downgrade():
    op.drop_column("moc_request_history", "other_aspects_required")
    op.drop_column("moc_requests", "other_aspects_required")
