"""Add userid FK to allowance_admission_child

Revision ID: ca2e625a2e74
Revises: a255ae96d130
Create Date: 2026-01-27 16:07:19.226338

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ca2e625a2e74'
down_revision: Union[str, Sequence[str], None] = 'a255ae96d130'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # -----------------------------
    # Main table: add column + FK
    # -----------------------------
    op.add_column(
        "allowance_admission_child",
        sa.Column("userid", sa.BigInteger(), nullable=True)
    )

    op.create_foreign_key(
        constraint_name="fk_allowance_admission_child_userid_users",
        source_table="allowance_admission_child",
        referent_table="users",
        local_cols=["userid"],
        remote_cols=["user_id"],
        ondelete="SET NULL"   # optional but recommended
    )

    # -----------------------------
    # History table: add column ONLY (NO FK)
    # -----------------------------
    op.add_column(
        "allowance_admission_child_history",
        sa.Column("userid", sa.BigInteger(), nullable=True)
    )


def downgrade():
    # -----------------------------
    # History table
    # -----------------------------
    op.drop_column("allowance_admission_child_history", "userid")

    # -----------------------------
    # Main table
    # -----------------------------
    op.drop_constraint(
        "fk_allowance_admission_child_userid_users",
        "allowance_admission_child",
        type_="foreignkey"
    )

    op.drop_column("allowance_admission_child", "userid")