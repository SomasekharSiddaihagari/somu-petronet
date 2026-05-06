"""add user supervisor to compoff

Revision ID: 1b0c64646d35
Revises: f0b67612edd9
Create Date: 2026-02-07 15:52:50.823337

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b0c64646d35'
down_revision: Union[str, Sequence[str], None] = 'f0b67612edd9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():

    # 🔵 MAIN TABLE
    op.add_column(
        'hr_leave_compof_day_new',
        sa.Column('user_id', sa.BigInteger(), nullable=True)
    )

    op.add_column(
        'hr_leave_compof_day_new',
        sa.Column('supervisor_id', sa.BigInteger(), nullable=True)
    )

    
   

    # 🔵 HISTORY TABLE
    op.add_column(
        'hr_leave_compof_day_new_history',
        sa.Column('user_id', sa.BigInteger(), nullable=True)
    )

    op.add_column(
        'hr_leave_compof_day_new_history',
        sa.Column('supervisor_id', sa.BigInteger(), nullable=True)
    )


def downgrade():

    # HISTORY
    op.drop_column('hr_leave_compof_day_new_history', 'supervisor_id')
    op.drop_column('hr_leave_compof_day_new_history', 'user_id')

    op.drop_column('hr_leave_compof_day_new', 'supervisor_id')
    op.drop_column('hr_leave_compof_day_new', 'user_id')
