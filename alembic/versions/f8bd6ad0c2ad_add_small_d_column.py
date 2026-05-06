"""add small d column

Revision ID: f8bd6ad0c2ad
Revises: c5be029c006c
Create Date: 2026-02-06 14:01:41.363240

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f8bd6ad0c2ad'
down_revision: Union[str, Sequence[str], None] = 'c5be029c006c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # user_finance
    op.execute("""
        ALTER TABLE user_finance 
        RENAME COLUMN "medical_insurance_80D" TO medical_insurance_80d;
    """)

    # user_finance_history
    op.execute("""
        ALTER TABLE user_finance_history 
        RENAME COLUMN "medical_insurance_80D" TO medical_insurance_80d;
    """)


def downgrade():
    op.execute("""
        ALTER TABLE user_finance 
        RENAME COLUMN medical_insurance_80d TO "medical_insurance_80D";
    """)

    op.execute("""
        ALTER TABLE user_finance_history 
        RENAME COLUMN medical_insurance_80d TO "medical_insurance_80D";
    """)