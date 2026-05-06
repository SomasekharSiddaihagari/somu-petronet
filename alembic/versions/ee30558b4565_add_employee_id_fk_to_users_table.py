"""add employee_id FK to users table

Revision ID: ee30558b4565
Revises: e8c5ffc2a321
Create Date: 2025-11-21 20:51:55.041925
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee30558b4565'
down_revision: Union[str, Sequence[str], None] = 'e8c5ffc2a321'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade: Add FK users.employee_id → employees.emp_id"""
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.create_foreign_key(
            "fk_users_employee_empid",
            "employees",
            ["employee_id"],  # column in users table
            ["emp_id"],       # PK in employees table
            ondelete="SET NULL"
        )


def downgrade() -> None:
    """Downgrade: Remove FK"""
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_constraint(
            "fk_users_employee_empid",
            type_="foreignkey"
        )
