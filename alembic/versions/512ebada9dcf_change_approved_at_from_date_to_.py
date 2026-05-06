"""change approved_at from date to datetime in outward_gate_pass tables

Revision ID: 512ebada9dcf
Revises: 5251412999cd
Create Date: 2026-03-16 21:04:55.697564

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '512ebada9dcf'
down_revision: Union[str, Sequence[str], None] = '5251412999cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    op.alter_column(
        "outward_gate_pass",
        "approved_at",
        existing_type=sa.Date(),
        type_=sa.DateTime(),
        existing_nullable=True
    )

    op.alter_column(
        "outward_gate_pass_history",
        "approved_at",
        existing_type=sa.Date(),
        type_=sa.DateTime(),
        existing_nullable=True
    )


def downgrade():

    op.alter_column(
        "outward_gate_pass",
        "approved_at",
        existing_type=sa.DateTime(),
        type_=sa.Date(),
        existing_nullable=True
    )

    op.alter_column(
        "outward_gate_pass_history",
        "approved_at",
        existing_type=sa.DateTime(),
        type_=sa.Date(),
        existing_nullable=True
    )
