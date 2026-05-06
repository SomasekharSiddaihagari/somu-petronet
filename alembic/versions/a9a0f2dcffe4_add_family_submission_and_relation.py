"""add family submission and relation

Revision ID: a9a0f2dcffe4
Revises: ac7713255bcb
Create Date: 2026-02-16 13:39:54.929486

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9a0f2dcffe4'
down_revision: Union[str, Sequence[str], None] = 'ac7713255bcb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    # ---------------------------
    # submission table
    # ---------------------------
    op.create_table(
        "submission",
        sa.Column("submission_id", sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(), nullable=True, server_default="Draft"),
        sa.Column("hr_comment", sa.String(), nullable=True),
        sa.Column("reviewed_by", sa.Integer(), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),

        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"]),
        sa.ForeignKeyConstraint(["reviewed_by"], ["users.user_id"]),
    )

    # ---------------------------
    # employee_family table changes
    # ---------------------------
    op.add_column(
        "employee_family",
        sa.Column("submission_id", sa.Integer(), nullable=True)
    )

    op.create_foreign_key(
        "fk_employee_family_submission",
        "employee_family",
        "submission",
        ["submission_id"],
        ["submission_id"],
        ondelete="SET NULL"
    )


def downgrade():

    # remove FK
    op.drop_constraint(
        "fk_employee_family_submission",
        "employee_family",
        type_="foreignkey"
    )

    # remove column
    op.drop_column("employee_family", "submission_id")

    # drop submission table
    op.drop_table("submission")