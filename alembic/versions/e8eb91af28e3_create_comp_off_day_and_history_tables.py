"""create comp off day and history tables

Revision ID: e8eb91af28e3
Revises: 3d25f8c2e763
Create Date: 2026-01-02 18:44:53.059768

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8eb91af28e3'
down_revision: Union[str, Sequence[str], None] = '3d25f8c2e763'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # MAIN TABLE
    op.create_table(
        "hr_leave_compof_day",
        sa.Column(
            "leave_compof_id",
            sa.BigInteger(),
            primary_key=True,
            autoincrement=True
        ),
        sa.Column(
            "leave_application_id",
            sa.BigInteger(),
            nullable=False
        ),
        sa.Column(
            "leave_date",
            sa.Date(),
            nullable=True
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False
        )
    )
 
    # HISTORY TABLE
    op.create_table(
        "hr_leave_compof_day_history",
        sa.Column(
            "history_id",
            sa.BigInteger(),
            primary_key=True,
            autoincrement=True
        ),
        sa.Column(
            "leave_compof_id",
            sa.BigInteger(),
            nullable=False
        ),
        sa.Column(
            "leave_application_id",
            sa.BigInteger(),
            nullable=False
        ),
        sa.Column(
            "leave_date",
            sa.Date(),
            nullable=True
        ),
        sa.Column(
            "action",
            sa.String(length=20),
            nullable=False
        ),
        sa.Column(
            "action_by",
            sa.BigInteger(),
            nullable=True
        ),
        sa.Column(
            "action_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False
        )
    )
 
    # Indexes (performance-safe)
    op.create_index(
        "ix_compof_day_leave_application_id",
        "hr_leave_compof_day",
        ["leave_application_id"]
    )
 
    op.create_index(
        "ix_compof_day_history_compof_id",
        "hr_leave_compof_day_history",
        ["leave_compof_id"]
    )
 
 
def downgrade():
    op.drop_index(
        "ix_compof_day_history_compof_id",
        table_name="hr_leave_compof_day_history"
    )
    op.drop_index(
        "ix_compof_day_leave_application_id",
        table_name="hr_leave_compof_day"
    )
 
    op.drop_table("hr_leave_compof_day_history")
    op.drop_table("hr_leave_compof_day")