"""add version to attachments and change audience version jsonb to string

Revision ID: c8bf6ce5bedd
Revises: b9a585256e72
Create Date: 2026-02-16 12:43:55.956011

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c8bf6ce5bedd'
down_revision: Union[str, Sequence[str], None] = 'b9a585256e72'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # =========================================
    # ADD version column to attachments tables
    # =========================================
    op.add_column(
        "circular_attachments",
        sa.Column("version", sa.String(length=50), nullable=True)
    )

    op.add_column(
        "circular_attachments_history",
        sa.Column("version", sa.String(length=50), nullable=True)
    )

    # ====================================================
    # CHANGE version column jsonb -> string (TEXT/VARCHAR)
    # circular_target_audience
    # ====================================================
    op.alter_column(
        "circular_target_audience",
        "version",
        existing_type=postgresql.JSONB(),
        type_=sa.String(length=50),
        postgresql_using="version::text",
    )

    op.alter_column(
        "circular_target_audience_history",
        "version",
        existing_type=postgresql.JSONB(),
        type_=sa.String(length=50),
        postgresql_using="version::text",
    )


def downgrade():
    # revert string -> jsonb
    op.alter_column(
        "circular_target_audience",
        "version",
        existing_type=sa.String(length=50),
        type_=postgresql.JSONB(),
        postgresql_using="version::jsonb",
    )

    op.alter_column(
        "circular_target_audience_history",
        "version",
        existing_type=sa.String(length=50),
        type_=postgresql.JSONB(),
        postgresql_using="version::jsonb",
    )

    # remove version from attachments
    op.drop_column("circular_attachments_history", "version")
    op.drop_column("circular_attachments", "version")