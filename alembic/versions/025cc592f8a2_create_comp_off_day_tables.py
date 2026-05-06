"""create comp off day tables

Revision ID: 025cc592f8a2
Revises: b735ac649360
Create Date: 2026-02-07 15:38:15.494451

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '025cc592f8a2'
down_revision: Union[str, Sequence[str], None] = 'b735ac649360'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    # MAIN TABLE
    op.create_table(
        'hr_leave_compof_day_new',

        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),

        sa.Column('employee_name', sa.String(length=150), nullable=True),
        sa.Column('employee_code', sa.String(length=50), nullable=True),

        sa.Column(
            'leave_application_id',
            sa.BigInteger(),
            sa.ForeignKey('hr_leave_application.leave_id', ondelete='CASCADE'),
            nullable=True
        ),

        sa.Column('leave_date', sa.Date(), nullable=True),
        sa.Column('station_id', sa.Integer(), nullable=True),
        sa.Column('type_id', sa.Integer(), nullable=True),

        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False
        )
    )

    # HISTORY TABLE
    op.create_table(
        'hr_leave_compof_day_new_history',

        sa.Column('history_id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('id', sa.BigInteger(), nullable=False),

        sa.Column('employee_name', sa.String(length=150), nullable=True),
        sa.Column('employee_code', sa.String(length=50), nullable=True),

        sa.Column('leave_application_id', sa.BigInteger(), nullable=True),
        sa.Column('leave_date', sa.Date(), nullable=True),

        sa.Column('station_id', sa.Integer(), nullable=True),
        sa.Column('type_id', sa.Integer(), nullable=True),

        sa.Column('action', sa.String(length=20), nullable=False),
        sa.Column('action_by', sa.String(length=100), nullable=True),

        sa.Column(
            'action_at',
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False
        )
    )


def downgrade():
    op.drop_table('hr_leave_compof_day_new_history')
    op.drop_table('hr_leave_compof_day_new')