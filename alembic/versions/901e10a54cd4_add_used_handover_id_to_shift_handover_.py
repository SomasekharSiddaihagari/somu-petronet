"""add used_handover_id to shift handover task tables

Revision ID: 901e10a54cd4
Revises: 9fdd63639e4b
Create Date: 2026-01-27 11:51:35.308210

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '901e10a54cd4'
down_revision: Union[str, Sequence[str], None] = '9fdd63639e4b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ---- shift_handover_task ----
    op.add_column(
        'shift_handover_task',
        sa.Column('used_handover_id', sa.Integer(), nullable=True)
    )

    op.create_foreign_key(
        'fk_shift_handover_task_used_handover_id',
        'shift_handover_task',
        'shift_handover_log',
        ['used_handover_id'],
        ['id'],
        ondelete='CASCADE'
    )

    # ---- shift_handover_task_history ----
    op.add_column(
        'shift_handover_task_history',
        sa.Column('used_handover_id', sa.Integer(), nullable=True)
    )

    op.create_foreign_key(
        'fk_shift_handover_task_history_used_handover_id',
        'shift_handover_task_history',
        'shift_handover_log',
        ['used_handover_id'],
        ['id'],
        ondelete='CASCADE'
    )