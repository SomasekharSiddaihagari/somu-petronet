"""create declaration_settings_history

Revision ID: 9bbcb70554e1
Revises: 6881d7d2f573
Create Date: 2025-11-25 16:05:15.113359

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9bbcb70554e1'
down_revision: Union[str, Sequence[str], None] = '6881d7d2f573'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.create_table(
        "declaration_settings_history",
        sa.Column("history_id", sa.Integer, primary_key=True),
        sa.Column("dec_id", sa.Integer),
        sa.Column("declaration_type", sa.String(length=50)),
        sa.Column("opening_date", sa.Date),
        sa.Column("closing_date", sa.Date),
        sa.Column("is_active", sa.Boolean),
        sa.Column("history_created_at", sa.DateTime)
    )
 
 
def downgrade():
    op.drop_table("declaration_settings_history")