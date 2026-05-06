"""change employee_type_id to employee_type

Revision ID: 4f3a771efd20
Revises: b5b9557b73c4
Create Date: 2025-11-28 18:06:22.542260

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4f3a771efd20'
down_revision: Union[str, Sequence[str], None] = 'b5b9557b73c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ---------------------------------------
    # leave_allocation_rules
    # ---------------------------------------
    op.alter_column(
        'leave_allocation_rules',
        'employee_type_id',
        new_column_name='employee_type',
        existing_type=sa.Integer(),
        type_=sa.String(),
        nullable=True
    )
 
    # ---------------------------------------
    # leave_allocation_rules_history
    # ---------------------------------------
    op.alter_column(
        'leave_allocation_rules_history',
        'employee_type_id',
        new_column_name='employee_type',
        existing_type=sa.Integer(),
        type_=sa.String(),
        nullable=True
    )
 
 
def downgrade():
    # Rollback if required
    op.alter_column(
        'leave_allocation_rules',
        'employee_type',
        new_column_name='employee_type_id',
        existing_type=sa.String(),
        type_=sa.Integer()
    )
 
    op.alter_column(
        'leave_allocation_rules_history',
        'employee_type',
        new_column_name='employee_type_id',
        existing_type=sa.String(),
        type_=sa.Integer()
    )