"""add cess self business fields to employee_form_12c

Revision ID: c6c9cb37983f
Revises: e35932ba25fc
Create Date: 2026-03-13 16:44:09.025193

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c6c9cb37983f'
down_revision: Union[str, Sequence[str], None] = 'e35932ba25fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    op.add_column(
        "employee_form_12c",
        sa.Column("self_cess_self_business", sa.String(), nullable=True)
    )

    op.add_column(
        "employee_form_12c",
        sa.Column("lo1_cess_self_business", sa.String(), nullable=True)
    )

    op.add_column(
        "employee_form_12c",
        sa.Column("lo2_cess_self_business", sa.String(), nullable=True)
    )

    # If history table also needs it
    op.add_column(
        "employee_form_12c_history",
        sa.Column("self_cess_self_business", sa.String(), nullable=True)
    )

    op.add_column(
        "employee_form_12c_history",
        sa.Column("lo1_cess_self_business", sa.String(), nullable=True)
    )

    op.add_column(
        "employee_form_12c_history",
        sa.Column("lo2_cess_self_business", sa.String(), nullable=True)
    )


def downgrade():

    op.drop_column("employee_form_12c", "self_cess_self_business")
    op.drop_column("employee_form_12c", "lo1_cess_self_business")
    op.drop_column("employee_form_12c", "lo2_cess_self_business")

    op.drop_column("employee_form_12c_history", "self_cess_self_business")
    op.drop_column("employee_form_12c_history", "lo1_cess_self_business")
    op.drop_column("employee_form_12c_history", "lo2_cess_self_business")
