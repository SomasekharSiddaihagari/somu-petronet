"""hse int

Revision ID: 7d37336a7bda
Revises: 47135cd22b08
Create Date: 2026-02-03 12:35:04.028201

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7d37336a7bda'
down_revision: Union[str, Sequence[str], None] = '47135cd22b08'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


TABLES = [
    "incident_report",
    "incident_report_history",
    "incident_prevention",
    "incident_prevention_history",
    "incident_investigation_team",
    "incident_investigation_team_history",
    "incident_impact_assessment",
    "incident_impact_assessment_history",
    "incident_cause_analysis",
    "incident_cause_analysis_history",
]


def upgrade():
    conn = op.get_bind()

    for table in TABLES:
        # 1️⃣ Clean non-numeric values → NULL
        conn.execute(sa.text(f"""
            UPDATE {table}
            SET created_by = NULL
            WHERE created_by IS NOT NULL
              AND created_by !~ '^[0-9]+$';
        """))

        conn.execute(sa.text(f"""
            UPDATE {table}
            SET updated_by = NULL
            WHERE updated_by IS NOT NULL
              AND updated_by !~ '^[0-9]+$';
        """))

        # 2️⃣ Alter column type safely
        with op.batch_alter_table(table) as batch_op:
            batch_op.alter_column(
                "created_by",
                existing_type=sa.String(length=100),
                type_=sa.Integer(),
                nullable=True,
                postgresql_using="created_by::integer",
            )

            batch_op.alter_column(
                "updated_by",
                existing_type=sa.String(length=100),
                type_=sa.Integer(),
                nullable=True,
                postgresql_using="updated_by::integer",
            )

def downgrade():
    for table in TABLES:
        with op.batch_alter_table(table) as batch_op:
            batch_op.alter_column(
                "created_by",
                existing_type=sa.Integer(),
                type_=sa.String(length=100),
                nullable=True,
                postgresql_using="created_by::text",
            )

            batch_op.alter_column(
                "updated_by",
                existing_type=sa.Integer(),
                type_=sa.String(length=100),
                nullable=True,
                postgresql_using="updated_by::text",
            )