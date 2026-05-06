"""add risk and project fields to hira tables

Revision ID: d83c147ad579
Revises: fabaa2ab3f7e
Create Date: 2026-02-02 10:19:33.131771

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd83c147ad579'
down_revision: Union[str, Sequence[str], None] = 'fabaa2ab3f7e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # hira_entries
    op.add_column(
        "hira_entries",
        sa.Column("risk", sa.String(length=100), nullable=True)
    )
    op.add_column(
        "hira_entries",
        sa.Column("division_dept_name", sa.String(length=255), nullable=True)
    )
    op.add_column(
        "hira_entries",
        sa.Column("project_requisition_no", sa.String(length=100), nullable=True)
    )
    op.add_column(
        "hira_entries",
        sa.Column("job_description", sa.Text(), nullable=True)
    )

    # hira_history
    op.add_column(
        "hira_history",
        sa.Column("risk", sa.String(length=100), nullable=True)
    )
    op.add_column(
        "hira_history",
        sa.Column("division_dept_name", sa.String(length=255), nullable=True)
    )
    op.add_column(
        "hira_history",
        sa.Column("project_requisition_no", sa.String(length=100), nullable=True)
    )
    op.add_column(
        "hira_history",
        sa.Column("job_description", sa.Text(), nullable=True)
    )


def downgrade():
    # hira_history
    op.drop_column("hira_history", "job_description")
    op.drop_column("hira_history", "project_requisition_no")
    op.drop_column("hira_history", "division_dept_name")
    op.drop_column("hira_history", "risk")

    # hira_entries
    op.drop_column("hira_entries", "job_description")
    op.drop_column("hira_entries", "project_requisition_no")
    op.drop_column("hira_entries", "division_dept_name")
    op.drop_column("hira_entries", "risk")