"""change tags jsonb to string

Revision ID: 829d94e66ad8
Revises: 20b1e7eb205f
Create Date: 2026-02-17 12:30:04.205746

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '829d94e66ad8'
down_revision: Union[str, Sequence[str], None] = '20b1e7eb205f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


tables = ["circular_master", "circular_master_history"]


def upgrade():
    for table in tables:
        op.alter_column(
            table,
            "tags",
            existing_type=sa.JSON(),
            type_=sa.String(),
            postgresql_using="tags::text"
        )


def downgrade():
    for table in tables:
        op.alter_column(
            table,
            "tags",
            existing_type=sa.String(),
            type_=sa.JSON(),
            postgresql_using="tags::jsonb"
        )