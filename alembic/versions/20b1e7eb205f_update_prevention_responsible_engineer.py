"""update prevention responsible engineer

Revision ID: 20b1e7eb205f
Revises: f5abd7a18406
Create Date: 2026-02-17 11:41:54.858045

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20b1e7eb205f'
down_revision: Union[str, Sequence[str], None] = 'f5abd7a18406'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


tables = [
    "incident_prevention",
    "incident_prevention_history"
]

def upgrade():
    for table in tables:

        # 🔁 rename allotted → responsible
        op.alter_column(
            table,
            "minor_allotted_engineer_name",
            new_column_name="minor_responsible_engineer_name"
        )

        op.alter_column(
            table,
            "minor_allotted_engineer_designation",
            new_column_name="minor_responsible_engineer_designation"
        )

        # 🔥 change created_by to INTEGER
        op.alter_column(
            table,
            "created_by",
            existing_type=sa.String(),
            type_=sa.Integer(),
            postgresql_using="created_by::integer"
        )

        op.alter_column(
            table,
            "updated_by",
            existing_type=sa.String(),
            type_=sa.Integer(),
            postgresql_using="updated_by::integer"
        )

        # ➕ add new columns
        op.add_column(table, sa.Column("minor_allotted_engineer_id", sa.Integer(), nullable=True))
        op.add_column(table, sa.Column("minor_allotted_responsible_id", sa.Integer(), nullable=True))


def downgrade():
    for table in tables:

        # rename back
        op.alter_column(
            table,
            "minor_responsible_engineer_name",
            new_column_name="minor_allotted_engineer_name"
        )

        op.alter_column(
            table,
            "minor_responsible_engineer_designation",
            new_column_name="minor_allotted_engineer_designation"
        )

        # int → string
        op.alter_column(
            table,
            "created_by",
            existing_type=sa.Integer(),
            type_=sa.String()
        )

        op.alter_column(
            table,
            "updated_by",
            existing_type=sa.Integer(),
            type_=sa.String()
        )

        # drop added
        op.drop_column(table, "minor_allotted_engineer_id")
        op.drop_column(table, "minor_allotted_responsible_id")