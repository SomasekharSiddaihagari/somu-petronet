"""Convert da_proof to TEXT

Revision ID: 73e9dc8dd23e
Revises: f14284729978
Create Date: 2025-12-10 20:35:20.375574

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '73e9dc8dd23e'
down_revision: Union[str, Sequence[str], None] = 'f14284729978'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # daily_allowance_sheet_detail.da_proof
    op.alter_column(
        'daily_allowance_sheet_detail',
        'da_proof',
        type_=sa.Text(),
        existing_type=sa.String(length=255),
        existing_nullable=True
    )

    # daily_allowance_sheet_detail_history.da_proof
    op.alter_column(
        'daily_allowance_sheet_detail_history',
        'da_proof',
        type_=sa.Text(),
        existing_type=sa.String(length=255),
        existing_nullable=True
    )


def downgrade():
    # Rollback to VARCHAR(255)
    op.alter_column(
        'daily_allowance_sheet_detail',
        'da_proof',
        type_=sa.String(length=255),
        existing_type=sa.Text(),
        existing_nullable=True
    )

    op.alter_column(
        'daily_allowance_sheet_detail_history',
        'da_proof',
        type_=sa.String(length=255),
        existing_type=sa.Text(),
        existing_nullable=True
    )