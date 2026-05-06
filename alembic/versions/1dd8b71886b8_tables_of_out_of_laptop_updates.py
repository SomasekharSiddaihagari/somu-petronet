"""tables of out of laptop updates

Revision ID: 1dd8b71886b8
Revises: 326b55162cfd
Create Date: 2025-12-29 16:44:36.140104

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1dd8b71886b8'
down_revision: Union[str, Sequence[str], None] = '326b55162cfd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ---- MAIN TABLE ----
    op.alter_column(
        "laptop_maintenance_reimbursement",
        column_name="annual_limit",
        new_column_name="total_claimed_amt",
        existing_type=sa.Numeric(12, 2),
    )

    # ---- HISTORY TABLE ----
    op.alter_column(
        "laptop_maintenance_reimbursement_history",
        column_name="annual_limit",
        new_column_name="total_claimed_amt",
        existing_type=sa.Numeric(12, 2),
    )


def downgrade():
    # ---- MAIN TABLE ----
    op.alter_column(
        "laptop_maintenance_reimbursement",
        column_name="total_claimed_amt",
        new_column_name="annual_limit",
        existing_type=sa.Numeric(12, 2),
    )

    # ---- HISTORY TABLE ----
    op.alter_column(
        "laptop_maintenance_reimbursement_history",
        column_name="total_claimed_amt",
        new_column_name="annual_limit",
        existing_type=sa.Numeric(12, 2),
    )