"""add allowance new fields

Revision ID: 6c1657a96ee6
Revises: bd34c7dc4348
Create Date: 2026-02-09 10:42:43.832286

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6c1657a96ee6'
down_revision: Union[str, Sequence[str], None] = 'bd34c7dc4348'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    # -------------------------------
    # allowance_claim
    # -------------------------------
    op.add_column(
        "allowance_claim",
        sa.Column("settling_no_of_days", sa.Integer(), nullable=True)
    )
    op.add_column(
        "allowance_claim",
        sa.Column("t_house_hold_rate", sa.Float(), nullable=True)
    )
    op.add_column(
        "allowance_claim",
        sa.Column("vehicle_rate", sa.Float(), nullable=True)
    )

    # -------------------------------
    # allowance_claim_history
    # -------------------------------
    op.add_column(
        "allowance_claim_history",
        sa.Column("settling_no_of_days", sa.Integer(), nullable=True)
    )
    op.add_column(
        "allowance_claim_history",
        sa.Column("t_house_hold_rate", sa.Float(), nullable=True)
    )
    op.add_column(
        "allowance_claim_history",
        sa.Column("vehicle_rate", sa.Float(), nullable=True)
    )

    # -------------------------------
    # allowance_admission_child
    # -------------------------------
    op.add_column(
        "allowance_admission_child",
        sa.Column("city_class", sa.String(length=100), nullable=True)
    )
    op.add_column(
        "allowance_admission_child",
        sa.Column("city_name", sa.String(length=150), nullable=True)
    )

    # -------------------------------
    # allowance_admission_child_history
    # -------------------------------
    op.add_column(
        "allowance_admission_child_history",
        sa.Column("city_class", sa.String(length=100), nullable=True)
    )
    op.add_column(
        "allowance_admission_child_history",
        sa.Column("city_name", sa.String(length=150), nullable=True)
    )


def downgrade():

    # allowance_claim
    op.drop_column("allowance_claim", "settling_no_of_days")
    op.drop_column("allowance_claim", "t_house_hold_rate")
    op.drop_column("allowance_claim", "vehicle_rate")

    # allowance_claim_history
    op.drop_column("allowance_claim_history", "settling_no_of_days")
    op.drop_column("allowance_claim_history", "t_house_hold_rate")
    op.drop_column("allowance_claim_history", "vehicle_rate")

    # allowance_admission_child
    op.drop_column("allowance_admission_child", "city_class")
    op.drop_column("allowance_admission_child", "city_name")

    # allowance_admission_child_history
    op.drop_column("allowance_admission_child_history", "city_class")
    op.drop_column("allowance_admission_child_history", "city_name")