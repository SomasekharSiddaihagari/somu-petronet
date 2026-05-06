"""Add comment_for_next_incharge to station_shift_incharge tables

Revision ID: 5e777d29db6a
Revises: be9e9ff4313e
Create Date: 2026-01-27 13:30:37.862826

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e777d29db6a'
down_revision: Union[str, Sequence[str], None] = 'be9e9ff4313e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    # Add column to main table
    op.add_column(
        "station_shift_incharge",
        sa.Column("comment_for_next_incharge", sa.String(), nullable=True)
    )

    # Add column to history table
    op.add_column(
        "station_shift_incharge_history",
        sa.Column("comment_for_next_incharge", sa.String(), nullable=True)
    )


def downgrade():
    # Remove column from history table
    op.drop_column("station_shift_incharge_history", "comment_for_next_incharge")

    # Remove column from main table
    op.drop_column("station_shift_incharge", "comment_for_next_incharge")