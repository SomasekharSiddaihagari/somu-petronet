"""add description fields for incident cause analysis

Revision ID: dee00085b8ef
Revises: 65d4a33f4155
Create Date: 2026-03-09 14:40:29.515778

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dee00085b8ef'
down_revision: Union[str, Sequence[str], None] = '65d4a33f4155'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    tables = [
        "incident_cause_analysis",
        "incident_cause_analysis_history"
    ]

    for table in tables:

        op.add_column(
            table,
            sa.Column(
                "leak_any_other_description",
                sa.Text(),
                nullable=True
            )
        )

        op.add_column(
            table,
            sa.Column(
                "ignition_any_other_pyrophoric_description",
                sa.Text(),
                nullable=True
            )
        )


def downgrade():

    tables = [
        "incident_cause_analysis",
        "incident_cause_analysis_history"
    ]

    for table in tables:

        op.drop_column(
            table,
            "ignition_any_other_pyrophoric_description"
        )

        op.drop_column(
            table,
            "leak_any_other_description"
        )
