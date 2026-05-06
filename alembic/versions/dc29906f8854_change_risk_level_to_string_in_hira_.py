"""Change risk_level to String in hira_history

Revision ID: dc29906f8854
Revises: 2a3ef39dfc77
Create Date: 2025-11-01 17:40:45.409482

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'dc29906f8854'
down_revision: Union[str, Sequence[str], None] = '2a3ef39dfc77'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ✅ Convert Enum to String safely without data loss
    with op.batch_alter_table('hira_history', schema=None) as batch_op:
        batch_op.alter_column(
            'risk_level',
            existing_type=sa.Enum('Low', 'Medium', 'High', 'Critical', name='risklevelenum'),
            type_=sa.String(length=50),
            existing_nullable=False
        )


def downgrade():
    # Optional rollback to Enum (not needed unless you plan to revert)
    risk_enum = sa.Enum('Low', 'Medium', 'High', 'Critical', name='risklevelenum')
    with op.batch_alter_table('hira_history', schema=None) as batch_op:
        batch_op.alter_column(
            'risk_level',
            existing_type=sa.String(length=50),
            type_=risk_enum,
            existing_nullable=False
        )