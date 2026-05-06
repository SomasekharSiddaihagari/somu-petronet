"""add g1 and g2 checklist fields

Revision ID: 2c02f7a8b7a2
Revises: 38173b013b1d
Create Date: 2026-03-07 18:16:19.099729

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c02f7a8b7a2'
down_revision: Union[str, Sequence[str], None] = '38173b013b1d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    tables = [
        "daily_safety_checklist",
        "daily_safety_checklist_history"
    ]

    for table in tables:

        op.add_column(
            table,
            sa.Column(
                "g1_product_leak_or_unsafe_condition",
                sa.Text(),
                nullable=True
            )
        )

        op.add_column(
            table,
            sa.Column(
                "g1_remarks",
                sa.Text(),
                nullable=True
            )
        )

        op.add_column(
            table,
            sa.Column(
                "g2_housekeeping_in_order",
                sa.Boolean(),
                nullable=True
            )
        )

        op.add_column(
            table,
            sa.Column(
                "g2_remarks",
                sa.Text(),
                nullable=True
            )
        )


def downgrade():

    tables = [
        "daily_safety_checklist",
        "daily_safety_checklist_history"
    ]

    for table in tables:

        op.drop_column(table, "g2_remarks")
        op.drop_column(table, "g2_housekeeping_in_order")
        op.drop_column(table, "g1_remarks")
        op.drop_column(table, "g1_product_leak_or_unsafe_condition")
