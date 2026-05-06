"""add is_employee to users and users_history

Revision ID: 1fae94c356c6
Revises: 7f9cc7b40b6f
Create Date: 2025-12-19 15:35:59.521260

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1fae94c356c6'
down_revision: Union[str, Sequence[str], None] = '7f9cc7b40b6f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add column to users table
    op.add_column(
        "users",
        sa.Column("is_employee", sa.Boolean(), nullable=False, server_default=sa.false())
    )

    # Add column to users_history table
    op.add_column(
        "users_history",
        sa.Column("is_employee", sa.Boolean(), nullable=False, server_default=sa.false())
    )


def downgrade():
    # Remove column from users_history table
    op.drop_column("users_history", "is_employee")

    # Remove column from users table
    op.drop_column("users", "is_employee")
