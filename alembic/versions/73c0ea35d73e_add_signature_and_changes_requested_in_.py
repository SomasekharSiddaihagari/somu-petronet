"""add signature and changes_requested_in fields

Revision ID: 73c0ea35d73e
Revises: 6fc3e65afaa8
Create Date: 2025-11-25 16:12:43.663691

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '73c0ea35d73e'
down_revision: Union[str, Sequence[str], None] = '6fc3e65afaa8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # ✅ Add signature column to user_asset_declaration_history
    op.add_column(
        "user_asset_declaration_history",
        sa.Column("signature", sa.Text(), nullable=True)
    )
 
    # ✅ Add changes_requested_in column to users table
    op.add_column(
        "users",
        sa.Column("changes_requested_in", sa.String(), nullable=True)
    )
 
    # ✅ Add changes_requested_in column to users_history table
    op.add_column(
        "users_history",
        sa.Column("changes_requested_in", sa.String(), nullable=True)
    )
 
 
def downgrade():
    # Rollback (optional)
 
    op.drop_column("user_asset_declaration_history", "signature")
    op.drop_column("users", "changes_requested_in")
    op.drop_column("users_history", "changes_requested_in")