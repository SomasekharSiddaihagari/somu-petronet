"""Add fuel config tables and fuel columns to vehicle reimbursement

Revision ID: f51ecabb2aff
Revises: ea13198c8610
Create Date: 2026-01-25 00:03:22.242293

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f51ecabb2aff'
down_revision: Union[str, Sequence[str], None] = 'ea13198c8610'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None




def upgrade():
    # ---------------------------------------
    # 1. Add column to vehicle_cm_reimbursement
    # ---------------------------------------


    # ---------------------------------------
    # 2. Create fuel_rate_config table
    # ---------------------------------------
    op.create_table(
        "fuel_rate_config",
        sa.Column("fuel_claim_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("petrol_rate", sa.Float(), nullable=True),
        sa.Column("others_rate", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now()
        ),
    )

    # ---------------------------------------
    # 3. Create fuel_rate_config_history table
    # ---------------------------------------
    op.create_table(
        "fuel_rate_config_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("fuel_claim_id", sa.Integer(), nullable=True),
        sa.Column("petrol_rate", sa.Float(), nullable=True),
        sa.Column("others_rate", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now()
        ),
    )


def downgrade():
    # ---------------------------------------
    # Drop history table
    # ---------------------------------------
    op.drop_table("fuel_rate_config_history")

    # ---------------------------------------
    # Drop main fuel rate table
    # ---------------------------------------
    op.drop_table("fuel_rate_config")

    # ---------------------------------------
    # Remove column from vehicle_cm_reimbursement
    # ---------------------------------------
    op.drop_column("vehicle_cm_reimbursement", "fixed_conveyance_claim")
