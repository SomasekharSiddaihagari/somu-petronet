"""add status and request meta to location_access_approval

Revision ID: f1a1da79b9b3
Revises: 58509655cd7a
Create Date: 2026-01-23 13:56:47.708533

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f1a1da79b9b3'
down_revision: Union[str, Sequence[str], None] = '58509655cd7a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ===== MAIN TABLE =====
   
    op.add_column(
        "location_access_approval",
        sa.Column("requested_ip", sa.String(length=45), nullable=True),
    )
    op.add_column(
        "location_access_approval",
        sa.Column("requested_latitude", sa.String(length=45), nullable=True),
    )
    op.add_column(
        "location_access_approval",
        sa.Column("requested_longitude", sa.String(length=45), nullable=True),
    )
    op.add_column(
        "location_access_approval",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=True,
        ),
    )

    # ===== HISTORY TABLE =====
    op.add_column(
        "location_access_approval_history",
        sa.Column("status", sa.String(length=50), nullable=True),
    )
    op.add_column(
        "location_access_approval_history",
        sa.Column("requested_ip", sa.String(length=45), nullable=True),
    )
    op.add_column(
        "location_access_approval_history",
        sa.Column("requested_latitude", sa.String(length=45), nullable=True),
    )
    op.add_column(
        "location_access_approval_history",
        sa.Column("requested_longitude", sa.String(length=45), nullable=True),
    )
    op.add_column(
        "location_access_approval_history",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )
