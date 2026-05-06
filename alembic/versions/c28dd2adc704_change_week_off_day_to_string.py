"""change week_off_day to string

Revision ID: c28dd2adc704
Revises: 9c73f329682a
Create Date: 2026-01-12 11:37:08.032630

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c28dd2adc704'
down_revision: Union[str, Sequence[str], None] = '9c73f329682a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        "employee_weekly_off",
        "week_off_day",
        existing_type=sa.SmallInteger(),
        type_=sa.Text(),
        existing_nullable=True,
        postgresql_using="week_off_day::text"
    )


def downgrade():
    op.alter_column(
        "employee_weekly_off",
        "week_off_day",
        existing_type=sa.Text(),
        type_=sa.SmallInteger(),
        existing_nullable=True,
        postgresql_using="week_off_day::integer"
    )