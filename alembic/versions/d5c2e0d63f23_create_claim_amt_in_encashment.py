"""create claim amt in encashment

Revision ID: d5c2e0d63f23
Revises: d1554a7c676e
Create Date: 2026-01-20 11:26:20.261724

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5c2e0d63f23'
down_revision: Union[str, Sequence[str], None] = 'd1554a7c676e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.add_column(
        "encashment_main_history",
        sa.Column("amount_claimed", sa.Numeric(12, 2), nullable=True)
    )

    op.add_column(
        "encashment_main",
        sa.Column("amount_claimed", sa.Numeric(12, 2), nullable=True)
    )

    op.add_column(
        "leave_encashment",
        sa.Column("amount_claimed", sa.Numeric(12, 2), nullable=True)
    )

    op.add_column(
        "leave_encashment_history",
        sa.Column("amount_claimed", sa.Numeric(12, 2), nullable=True)
    )


def downgrade():
    op.drop_column("leave_encashment_history", "amount_claimed")
    op.drop_column("leave_encashment", "amount_claimed")
    op.drop_column("encashment_main", "amount_claimed")
    op.drop_column("encashment_main_history", "amount_claimed")