"""add reviewer and address fields

Revision ID: 743e3208a1bd
Revises: c42403a622a9
Create Date: 2026-02-18 00:47:00.199507

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '743e3208a1bd'
down_revision: Union[str, Sequence[str], None] = 'c42403a622a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    # ===============================
    # returnable_gate_pass table
    # ===============================
    op.add_column(
        "returnable_gate_pass",
        sa.Column("reviewer_id", sa.Integer(), nullable=True)
    )

    # ===============================
    # users table
    # ===============================
    op.add_column(
        "users",
        sa.Column("pr_address_document_details", sa.Text(), nullable=True)
    )

    op.add_column(
        "users",
        sa.Column("cr_address_comment", sa.Text(), nullable=True)
    )

    # ===============================
    # users_history table
    # ===============================
    op.add_column(
        "users_history",
        sa.Column("pr_address_document_details", sa.Text(), nullable=True)
    )

    op.add_column(
        "users_history",
        sa.Column("cr_address_comment", sa.Text(), nullable=True)
    )


def downgrade():

    # users_history
    op.drop_column("users_history", "cr_address_comment")
    op.drop_column("users_history", "pr_address_document_details")

    # users
    op.drop_column("users", "cr_address_comment")
    op.drop_column("users", "pr_address_document_details")

    # returnable_gate_pass
    op.drop_column("returnable_gate_pass", "reviewer_id")
