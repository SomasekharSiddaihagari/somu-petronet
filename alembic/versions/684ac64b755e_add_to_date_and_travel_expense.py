"""add to_date and travel expense

Revision ID: 684ac64b755e
Revises: 4d7cc0f0b10c
Create Date: 2026-02-09 19:05:17.428179

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '684ac64b755e'
down_revision: Union[str, Sequence[str], None] = '4d7cc0f0b10c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    # ➕ add to_date to travel child table
    op.add_column('travel_requisition_travel',
        sa.Column('to_date', sa.Date(), nullable=True)
    )

    op.add_column('travel_requisition_travel_history',
        sa.Column('to_date', sa.Date(), nullable=True)
    )

    # ❌ remove from main table
    op.drop_column('travel_requisition', 'to_date')
    op.drop_column('travel_requisition_history', 'to_date')


def downgrade():

    op.add_column('travel_requisition',
        sa.Column('to_date', sa.Date(), nullable=True)
    )

    op.add_column('travel_requisition_history',
        sa.Column('to_date', sa.Date(), nullable=True)
    )

    op.drop_column('travel_requisition_travel', 'to_date')
    op.drop_column('travel_requisition_travel_history', 'to_date')