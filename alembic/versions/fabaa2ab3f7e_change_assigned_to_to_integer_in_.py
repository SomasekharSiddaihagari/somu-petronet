"""change assigned_to to integer in logbook shift tables

Revision ID: fabaa2ab3f7e
Revises: 7d2059604fb5
Create Date: 2026-01-31 18:12:10.152180

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fabaa2ab3f7e'
down_revision: Union[str, Sequence[str], None] = '7d2059604fb5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # logbook_shift_master
    op.alter_column(
        "logbook_shift_master",
        "assigned_to",
        existing_type=sa.String(length=100),
        type_=sa.Integer(),
        postgresql_using="assigned_to::integer",
        nullable=True,
    )

    # logbook_shift_master_history
    op.alter_column(
        "logbook_shift_master_history",
        "assigned_to",
        existing_type=sa.String(length=100),
        type_=sa.Integer(),
        postgresql_using="assigned_to::integer",
        nullable=True,
    )


def downgrade():
    # logbook_shift_master_history
    op.alter_column(
        "logbook_shift_master_history",
        "assigned_to",
        existing_type=sa.Integer(),
        type_=sa.String(length=100),
        postgresql_using="assigned_to::text",
        nullable=True,
    )

    # logbook_shift_master
    op.alter_column(
        "logbook_shift_master",
        "assigned_to",
        existing_type=sa.Integer(),
        type_=sa.String(length=100),
        postgresql_using="assigned_to::text",
        nullable=True,
    )