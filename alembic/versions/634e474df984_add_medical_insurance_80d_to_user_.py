"""add medical_insurance_80D to user_finance tables

Revision ID: 634e474df984
Revises: 559a667b1cd9
Create Date: 2026-02-06 13:12:06.470220

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '634e474df984'
down_revision: Union[str, Sequence[str], None] = '559a667b1cd9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # user_finance table
    op.add_column(
        'user_finance',
        sa.Column('medical_insurance_80D', sa.Numeric(), nullable=True)
    )

    # user_finance_history table
    op.add_column(
        'user_finance_history',
        sa.Column('medical_insurance_80D', sa.Numeric(), nullable=True)
    )


def downgrade():
    op.drop_column('user_finance', 'medical_insurance_80D')
    op.drop_column('user_finance_history', 'medical_insurance_80D')