"""add is_used column to compoff tables

Revision ID: 06389f4afa0e
Revises: 901fdc2d2d6c
Create Date: 2026-02-10 13:26:14.268145

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '06389f4afa0e'
down_revision: Union[str, Sequence[str], None] = '901fdc2d2d6c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        'hr_leave_compof_day_new',
        sa.Column('is_used', sa.Boolean(), nullable=True, server_default='false')
    )

    op.add_column(
        'hr_leave_compof_day_new_history',
        sa.Column('is_used', sa.Boolean(), nullable=True, server_default='false')
    )


def downgrade():
    op.drop_column('hr_leave_compof_day_new', 'is_used')
    op.drop_column('hr_leave_compof_day_new_history', 'is_used')