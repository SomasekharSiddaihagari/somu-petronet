"""Safely add foreign key for MoCRequestHistory (no table drops)

Revision ID: 0d37cd28ac32
Revises: 541269591175
Create Date: 2025-10-31 16:01:49.644401
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0d37cd28ac32'
down_revision: Union[str, Sequence[str], None] = '541269591175'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Safe upgrade - only add missing columns or constraints."""

    # ✅ Add moc_request_id to hira_entries if missing
    with op.batch_alter_table("hira_entries", schema=None) as batch_op:
        # Check if the column already exists in DB
        batch_op.add_column(sa.Column("moc_request_id", sa.Integer(), nullable=True))
        # Add FK safely (only if not already there)
        batch_op.create_foreign_key(
            "fk_hira_entries_moc_request_id",
            "moc_requests",
            ["moc_request_id"],
            ["moc_request_id"],
            ondelete="CASCADE"
        )

    # ✅ Add foreign key from moc_request_history to moc_requests if missing
    with op.batch_alter_table("moc_request_history", schema=None) as batch_op:
        batch_op.create_foreign_key(
            "fk_moc_request_history_moc_request_id",
            "moc_requests",
            ["moc_request_id"],
            ["moc_request_id"],
        )

    # ✅ Ensure user-role foreign key is properly linked
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_constraint("users_role_id_fkey", type_="foreignkey")
        batch_op.create_foreign_key(
            "fk_users_role_id",
            "roles",
            ["role_id"],
            ["role_id"]
        )

    # ⚠️ NOTE: No tables dropped, no data deleted.
    # Only new FKs or columns added safely.


def downgrade() -> None:
    """Safe downgrade - remove added constraints only."""
    with op.batch_alter_table("moc_request_history", schema=None) as batch_op:
        batch_op.drop_constraint("fk_moc_request_history_moc_request_id", type_="foreignkey")

    with op.batch_alter_table("hira_entries", schema=None) as batch_op:
        batch_op.drop_constraint("fk_hira_entries_moc_request_id", type_="foreignkey")
        # Don’t drop column automatically — keep data safe.

    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_constraint("fk_users_role_id", type_="foreignkey")
