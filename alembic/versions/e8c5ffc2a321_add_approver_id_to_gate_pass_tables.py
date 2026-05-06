"""Add approver_id to gate pass tables

Revision ID: e8c5ffc2a321
Revises: e286525c91b3
Create Date: 2025-11-14 22:06:19.291360
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'e8c5ffc2a321'
down_revision: Union[str, Sequence[str], None] = 'e286525c91b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- InwardGatePassHistory ---
    with op.batch_alter_table("inward_gate_pass_history", schema=None) as batch_op:
        batch_op.add_column(sa.Column("approver_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            "fk_inward_history_approver_id",
            "users",
            ["approver_id"],
            ["user_id"],
            ondelete="SET NULL",
        )

    # --- InwardGatePass ---
    with op.batch_alter_table("inward_gate_pass", schema=None) as batch_op:
        batch_op.add_column(sa.Column("approver_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            "fk_inward_approver_id",
            "users",
            ["approver_id"],
            ["user_id"],
            ondelete="SET NULL",
        )

    # --- OutwardGatePassHistory ---
    with op.batch_alter_table("outward_gate_pass_history", schema=None) as batch_op:
        batch_op.add_column(sa.Column("approver_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            "fk_outward_history_approver_id",
            "users",
            ["approver_id"],
            ["user_id"],
            ondelete="SET NULL",
        )

    # --- OutwardGatePass ---
    with op.batch_alter_table("outward_gate_pass", schema=None) as batch_op:
        batch_op.add_column(sa.Column("approver_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            "fk_outward_approver_id",
            "users",
            ["approver_id"],
            ["user_id"],
            ondelete="SET NULL",
        )


def downgrade() -> None:
    # Reverse the upgrade safely
    with op.batch_alter_table("inward_gate_pass_history", schema=None) as batch_op:
        batch_op.drop_constraint("fk_inward_history_approver_id", type_="foreignkey")
        batch_op.drop_column("approver_id")

    with op.batch_alter_table("inward_gate_pass", schema=None) as batch_op:
        batch_op.drop_constraint("fk_inward_approver_id", type_="foreignkey")
        batch_op.drop_column("approver_id")

    with op.batch_alter_table("outward_gate_pass_history", schema=None) as batch_op:
        batch_op.drop_constraint("fk_outward_history_approver_id", type_="foreignkey")
        batch_op.drop_column("approver_id")

    with op.batch_alter_table("outward_gate_pass", schema=None) as batch_op:
        batch_op.drop_constraint("fk_outward_approver_id", type_="foreignkey")
        batch_op.drop_column("approver_id")
