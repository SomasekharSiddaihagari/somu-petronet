"""create employee_bank and employee_bank_history tables

Revision ID: 6ab26a548b9d
Revises: 0277f082b522
Create Date: 2026-02-13 20:13:30.015180

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ab26a548b9d'
down_revision: Union[str, Sequence[str], None] = '0277f082b522'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ---------------------------------------------------------
    # employee_bank table
    # ---------------------------------------------------------
    op.create_table(
        "employee_bank",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.user_id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("bank_name", sa.String(), nullable=True),
        sa.Column("branch_name", sa.String(), nullable=True),
        sa.Column("account_number", sa.String(), nullable=True),
        sa.Column("ifsc_code", sa.String(), nullable=True),
        sa.Column("account_holder_name", sa.String(), nullable=True),
        sa.Column("account_type", sa.String(), nullable=True),
        sa.Column("cancelled_cheque", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column("remarks", sa.Text(), nullable=True),
    )

    # ---------------------------------------------------------
    # employee_bank_history table
    # ---------------------------------------------------------
    op.create_table(
        "employee_bank_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, index=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("bank_name", sa.String(), nullable=True),
        sa.Column("branch_name", sa.String(), nullable=True),
        sa.Column("account_number", sa.String(), nullable=True),
        sa.Column("ifsc_code", sa.String(), nullable=True),
        sa.Column("account_holder_name", sa.String(), nullable=True),
        sa.Column("account_type", sa.String(), nullable=True),
        sa.Column("cancelled_cheque", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column("remarks", sa.Text(), nullable=True),
    )


def downgrade():
    op.drop_table("employee_bank_history")
    op.drop_table("employee_bank")