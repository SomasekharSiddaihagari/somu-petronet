"""add comments to leave encashment tables

Revision ID: a7089de74f37
Revises: b7ac56d384f2
Create Date: 2026-01-14 12:18:02.461698

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7089de74f37'
down_revision: Union[str, Sequence[str], None] = 'b7ac56d384f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # -------- leave_encashment --------
    op.add_column(
        "leave_encashment",
        sa.Column("finance_comment", sa.Text(), nullable=True),
    )
    op.add_column(
        "leave_encashment",
        sa.Column("hr_comment", sa.Text(), nullable=True),
    )
    op.add_column(
        "leave_encashment",
        sa.Column("supervisor_comment", sa.Text(), nullable=True),
    )

    # -------- leave_encashment_history --------
    op.add_column(
        "leave_encashment_history",
        sa.Column("finance_comment", sa.Text(), nullable=True),
    )
    op.add_column(
        "leave_encashment_history",
        sa.Column("hr_comment", sa.Text(), nullable=True),
    )
    op.add_column(
        "leave_encashment_history",
        sa.Column("supervisor_comment", sa.Text(), nullable=True),
    )


def downgrade():
    # -------- leave_encashment_history --------
    op.drop_column("leave_encashment_history", "supervisor_comment")
    op.drop_column("leave_encashment_history", "hr_comment")
    op.drop_column("leave_encashment_history", "finance_comment")

    # -------- leave_encashment --------
    op.drop_column("leave_encashment", "supervisor_comment")
    op.drop_column("leave_encashment", "hr_comment")
    op.drop_column("leave_encashment", "finance_comment")