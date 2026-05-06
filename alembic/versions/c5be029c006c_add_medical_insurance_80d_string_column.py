"""add medical_insurance_80D string column

Revision ID: c5be029c006c
Revises: 634e474df984
Create Date: 2026-02-06 13:39:07.814181

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c5be029c006c'
down_revision: Union[str, Sequence[str], None] = '634e474df984'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    # user_finance
    op.execute("""
        ALTER TABLE user_finance 
        ALTER COLUMN "medical_insurance_80D" 
        TYPE VARCHAR 
        USING "medical_insurance_80D"::text;
    """)

    # user_finance_history
    op.execute("""
        ALTER TABLE user_finance_history 
        ALTER COLUMN "medical_insurance_80D" 
        TYPE VARCHAR 
        USING "medical_insurance_80D"::text;
    """)

def downgrade():
    op.execute("""
        ALTER TABLE user_finance 
        ALTER COLUMN "medical_insurance_80D" 
        TYPE NUMERIC 
        USING "medical_insurance_80D"::numeric;
    """)

    op.execute("""
        ALTER TABLE user_finance_history 
        ALTER COLUMN "medical_insurance_80D" 
        TYPE NUMERIC 
        USING "medical_insurance_80D"::numeric;
    """)