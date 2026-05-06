"""add submenu allowed roles table

Revision ID: 1e1034434ed6
Revises: 1fae94c356c6
Create Date: 2025-12-19 18:55:25.671909

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e1034434ed6'
down_revision: Union[str, Sequence[str], None] = '1fae94c356c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "submenu_allowed_roles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("submenu_id", sa.Integer(), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=False),
 
        sa.ForeignKeyConstraint(
            ["submenu_id"],
            ["submenus.submenu_id"],
            ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["roles.role_id"],
            ondelete="CASCADE"
        ),
 
        sa.UniqueConstraint(
            "submenu_id",
            "role_id",
            name="uq_submenu_role"
        )
    )
 
 
def downgrade():
    op.drop_table("submenu_allowed_roles")
