"""add annual_limit to laptop maintenance reimbursement

Revision ID: 77f1a6786c44
Revises: 8480797f7970
Create Date: 2025-12-30 15:51:30.772307

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '77f1a6786c44'
down_revision: Union[str, Sequence[str], None] = '8480797f7970'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.add_column(
        "laptop_maintenance_reimbursement",
        sa.Column("annual_limit", sa.Numeric(12, 2), nullable=True)
    )

    op.add_column(
        "laptop_maintenance_reimbursement_history",
        sa.Column("annual_limit", sa.Numeric(12, 2), nullable=True)
    )


def downgrade():
    op.drop_column(
        "laptop_maintenance_reimbursement_history",
        "annual_limit"
    )

    op.drop_column(
        "laptop_maintenance_reimbursement",
        "annual_limit"
    )