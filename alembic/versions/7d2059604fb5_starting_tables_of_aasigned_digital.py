"""starting tables of aasigned  digital

Revision ID: 7d2059604fb5
Revises: a6d90dd7982f
Create Date: 2026-01-31 18:07:18.333243

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7d2059604fb5'
down_revision: Union[str, Sequence[str], None] = 'a6d90dd7982f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # logbook_shift_master
    op.add_column(
        "logbook_shift_master",
        sa.Column("assigned_to", sa.String(length=100), nullable=True),
    )

    # logbook_shift_master_history
    op.add_column(
        "logbook_shift_master_history",
        sa.Column("assigned_to", sa.String(length=100), nullable=True),
    )


def downgrade():
    # logbook_shift_master_history
    op.drop_column("logbook_shift_master_history", "assigned_to")

    # logbook_shift_master
    op.drop_column("logbook_shift_master", "assigned_to")