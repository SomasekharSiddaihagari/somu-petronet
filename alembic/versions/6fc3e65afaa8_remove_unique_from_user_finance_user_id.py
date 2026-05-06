"""remove unique from user_finance user_id

Revision ID: 6fc3e65afaa8
Revises: 9bbcb70554e1
Create Date: 2025-11-25 16:06:57.018615

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6fc3e65afaa8'
down_revision: Union[str, Sequence[str], None] = '9bbcb70554e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # ✅ Drop the unique constraint on user_id
    op.drop_constraint(
        "user_finance_user_id_key",  # common auto name in Postgres
        "user_finance",
        type_="unique"
    )
 
 
def downgrade():
    # ✅ Re-add unique constraint if needed
    op.create_unique_constraint(
        "user_finance_user_id_key",
        "user_finance",
        ["user_id"]
    )