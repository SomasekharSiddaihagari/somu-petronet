"""emp week off

Revision ID: 50948a079bc3
Revises: d63ae686ddee
Create Date: 2026-01-08 18:03:05.683253

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50948a079bc3'
down_revision: Union[str, Sequence[str], None] = 'd63ae686ddee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "employee_weekly_off",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column("user_id", sa.BigInteger, nullable=True),
        sa.Column("week_off_day", sa.SmallInteger, nullable=True),
        sa.Column("effective_from", sa.Date, nullable=True),
        sa.Column("effective_to", sa.Date, nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=True, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column(
            "updated_at",
            sa.DateTime,
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
    )
 
    op.create_index(
        "idx_employee_weekly_off_user",
        "employee_weekly_off",
        ["user_id", "effective_from", "effective_to", "is_active"],
    )
 
 
def downgrade():
    op.drop_index("idx_employee_weekly_off_user", table_name="employee_weekly_off")
    op.drop_table("employee_weekly_off")