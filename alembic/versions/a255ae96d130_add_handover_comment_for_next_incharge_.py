"""Add handover comment_for_next_incharge to station_shift_incha

Revision ID: a255ae96d130
Revises: 5e777d29db6a
Create Date: 2026-01-27 13:54:15.813051

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a255ae96d130'
down_revision: Union[str, Sequence[str], None] = '5e777d29db6a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Add column to main table
    op.add_column(
        'shift_handover_log',
        sa.Column('comment_for_next_incharge', sa.String(length=255), nullable=True)
    )

    # Add column to history table
    op.add_column(
        'shift_handover_log_history',
        sa.Column('comment_for_next_incharge', sa.String(length=255), nullable=True)
    )


def downgrade():
    # Remove column from main table
    op.drop_column('shift_handover_log', 'comment_for_next_incharge')

    # Remove column from history table
    op.drop_column('shift_handover_log_history', 'comment_for_next_incharge')