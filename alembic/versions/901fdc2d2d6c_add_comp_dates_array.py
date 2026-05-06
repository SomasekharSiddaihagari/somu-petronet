"""add comp_dates array

Revision ID: 901fdc2d2d6c
Revises: 684ac64b755e
Create Date: 2026-02-09 19:43:02.569088

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '901fdc2d2d6c'
down_revision: Union[str, Sequence[str], None] = '684ac64b755e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        'hr_leave_application',
        sa.Column('comp_dates', postgresql.ARRAY(sa.Date()), nullable=True)
    )

    op.add_column(
        'hr_leave_application_history',
        sa.Column('comp_dates', postgresql.ARRAY(sa.Date()), nullable=True)
    )


def downgrade():
    op.drop_column('hr_leave_application', 'comp_dates')
    op.drop_column('hr_leave_application_history', 'comp_dates')