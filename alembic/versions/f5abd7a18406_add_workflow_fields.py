"""add workflow fields

Revision ID: f5abd7a18406
Revises: 296d1349a83b
Create Date: 2026-02-17 11:22:29.289730

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f5abd7a18406'
down_revision: Union[str, Sequence[str], None] = '296d1349a83b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



# 🔥 tables list
tables = [
    "incident_report",
    "incident_report_history",
    "incident_prevention",
    "incident_prevention_history"
]


def upgrade():
    for table in tables:

        # =========================
        # MINOR WORKFLOW
        # =========================
        op.add_column(table, sa.Column("minor_sic_name", sa.String(150), nullable=True))
        op.add_column(table, sa.Column("minor_sic_updated_date", sa.Date(), nullable=True))

        op.add_column(table, sa.Column("minor_alloted_engineer_name", sa.String(150), nullable=True))
        op.add_column(table, sa.Column("minor_alloted_eng_updated_date", sa.Date(), nullable=True))

        op.add_column(table, sa.Column("minor_final_approve_name", sa.String(150), nullable=True))
        op.add_column(table, sa.Column("minor_final_approved_date", sa.Date(), nullable=True))


        # =========================
        # MAJOR WORKFLOW
        # =========================
        op.add_column(table, sa.Column("major_team_leader_by", sa.String(150), nullable=True))
        op.add_column(table, sa.Column("major_team_leader_date", sa.Date(), nullable=True))

        op.add_column(table, sa.Column("major_team_acknowledged_by", sa.String(150), nullable=True))
        op.add_column(table, sa.Column("major_team_acknowledged_date", sa.Date(), nullable=True))

        op.add_column(table, sa.Column("major_report_filled_by", sa.String(150), nullable=True))
        op.add_column(table, sa.Column("major_report_filled_date", sa.Date(), nullable=True))

        op.add_column(table, sa.Column("major_investigation_ack_by", sa.String(150), nullable=True))
        op.add_column(table, sa.Column("major_investigation_ack_date", sa.Date(), nullable=True))

        op.add_column(table, sa.Column("major_safety_officer_by", sa.String(150), nullable=True))
        op.add_column(table, sa.Column("major_safety_officer_date", sa.Date(), nullable=True))

        op.add_column(table, sa.Column("major_md_review_by", sa.String(150), nullable=True))
        op.add_column(table, sa.Column("major_md_review_date", sa.Date(), nullable=True))

        op.add_column(table, sa.Column("major_hse_review_by", sa.String(150), nullable=True))
        op.add_column(table, sa.Column("major_hse_review_date", sa.Date(), nullable=True))

        op.add_column(table, sa.Column("major_capa_filled_by", sa.String(150), nullable=True))
        op.add_column(table, sa.Column("major_capa_filled_date", sa.Date(), nullable=True))

        op.add_column(table, sa.Column("major_hse_capa_review_by", sa.String(150), nullable=True))
        op.add_column(table, sa.Column("major_hse_capa_review_date", sa.Date(), nullable=True))

        op.add_column(table, sa.Column("major_closure_by", sa.String(150), nullable=True))
        op.add_column(table, sa.Column("major_closure_date", sa.Date(), nullable=True))


def downgrade():
    for table in tables:

        # MINOR
        op.drop_column(table, "minor_sic_name")
        op.drop_column(table, "minor_sic_updated_date")

        op.drop_column(table, "minor_alloted_engineer_name")
        op.drop_column(table, "minor_alloted_eng_updated_date")

        op.drop_column(table, "minor_final_approve_name")
        op.drop_column(table, "minor_final_approved_date")

        # MAJOR
        op.drop_column(table, "major_team_leader_by")
        op.drop_column(table, "major_team_leader_date")

        op.drop_column(table, "major_team_acknowledged_by")
        op.drop_column(table, "major_team_acknowledged_date")

        op.drop_column(table, "major_report_filled_by")
        op.drop_column(table, "major_report_filled_date")

        op.drop_column(table, "major_investigation_ack_by")
        op.drop_column(table, "major_investigation_ack_date")

        op.drop_column(table, "major_safety_officer_by")
        op.drop_column(table, "major_safety_officer_date")

        op.drop_column(table, "major_md_review_by")
        op.drop_column(table, "major_md_review_date")

        op.drop_column(table, "major_hse_review_by")
        op.drop_column(table, "major_hse_review_date")

        op.drop_column(table, "major_capa_filled_by")
        op.drop_column(table, "major_capa_filled_date")

        op.drop_column(table, "major_hse_capa_review_by")
        op.drop_column(table, "major_hse_capa_review_date")

        op.drop_column(table, "major_closure_by")
        op.drop_column(table, "major_closure_date")