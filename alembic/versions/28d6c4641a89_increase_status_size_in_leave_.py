"""increase status size in leave encashment tables

Revision ID: 28d6c4641a89
Revises: a7089de74f37
Create Date: 2026-01-14 12:55:42.738122

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28d6c4641a89'
down_revision: Union[str, Sequence[str], None] = 'a7089de74f37'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # -------- leave_encashment --------
    op.alter_column(
        "leave_encashment",
        "status",
        type_=sa.String(length=256),
        existing_type=sa.String(length=30),
        existing_nullable=True,
    )

    # -------- leave_encashment_history --------
    op.alter_column(
        "leave_encashment_history",
        "status",
        type_=sa.String(length=256),
        existing_type=sa.String(length=30),
        existing_nullable=True,
    )


def downgrade():
    # rollback to 30 chars
    op.alter_column(
        "leave_encashment",
        "status",
        type_=sa.String(length=30),
        existing_type=sa.String(length=256),
        existing_nullable=True,
    )

    op.alter_column(
        "leave_encashment_history",
        "status",
        type_=sa.String(length=30),
        existing_type=sa.String(length=256),
        existing_nullable=True,
    )
