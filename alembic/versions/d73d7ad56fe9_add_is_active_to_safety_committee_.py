"""add is_active to safety committee minutes tables

Revision ID: d73d7ad56fe9
Revises: 20086854bac1
Create Date: 2026-02-18 17:41:05.529550

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd73d7ad56fe9'
down_revision: Union[str, Sequence[str], None] = '20086854bac1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        'safety_committee_minutes',
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.true())
    )

    op.add_column(
        'safety_committee_minutes_history',
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.true())
    )

    # remove default after adding (optional best practice)
    op.alter_column('safety_committee_minutes', 'is_active', server_default=None)
    op.alter_column('safety_committee_minutes_history', 'is_active', server_default=None)


def downgrade():
    op.drop_column('safety_committee_minutes', 'is_active')
    op.drop_column('safety_committee_minutes_history', 'is_active')