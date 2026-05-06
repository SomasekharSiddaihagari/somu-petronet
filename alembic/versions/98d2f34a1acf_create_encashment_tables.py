"""create encashment tables

Revision ID: 98d2f34a1acf
Revises: 70e263142a4e
Create Date: 2026-01-21 13:33:17.588206

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '98d2f34a1acf'
down_revision: Union[str, Sequence[str], None] = '70e263142a4e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # leave_encashment
    op.add_column(
        "leave_encashment",
        sa.Column("no_days_approved", sa.Numeric(12, 2), nullable=True)
    )

    # encashment_main
    op.add_column(
        "encashment_main",
        sa.Column("no_days_approved", sa.Numeric(12, 2), nullable=True)
    )


def downgrade():
    op.drop_column("encashment_main", "no_days_approved")
    op.drop_column("leave_encashment", "no_days_approved")