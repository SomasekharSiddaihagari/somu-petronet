"""rename brought_back_date to bought_back_date

Revision ID: 1d7a012baf76
Revises: 1c77bd4e3b1e
Create Date: 2026-01-12 14:50:37.588295

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d7a012baf76'
down_revision: Union[str, Sequence[str], None] = '1c77bd4e3b1e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # asset_claim
    op.alter_column(
        "asset_claim",
        "brought_back_date",
        new_column_name="bought_back_date",
        existing_type=sa.Date()
    )

    # asset_claim_history
    op.alter_column(
        "asset_claim_history",
        "brought_back_date",
        new_column_name="bought_back_date",
        existing_type=sa.Date()
    )


def downgrade():
    # revert names back

    op.alter_column(
        "asset_claim",
        "bought_back_date",
        new_column_name="brought_back_date",
        existing_type=sa.Date()
    )

    op.alter_column(
        "asset_claim_history",
        "bought_back_date",
        new_column_name="brought_back_date",
        existing_type=sa.Date()
    )
