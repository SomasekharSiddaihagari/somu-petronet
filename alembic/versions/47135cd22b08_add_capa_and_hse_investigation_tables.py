"""add capa tables and extend hse investigation tables

Revision ID: 47135cd22b08
Revises: a8ad1df38dea
Create Date: 2026-02-02
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = "47135cd22b08"
down_revision: Union[str, Sequence[str], None] = "a8ad1df38dea"
branch_labels = None
depends_on = None





def upgrade():

    # =====================================================
    # 🔧 HSE INCIDENT INVESTIGATION MASTER (ADD COLUMN)
    # =====================================================
    op.add_column(
        "hse_incident_investigation_master",
        sa.Column("incident_id", sa.Integer(), nullable=False)
    )

    op.create_foreign_key(
        "fk_hse_investigation_incident",
        "hse_incident_investigation_master",
        "incident_report",
        ["incident_id"],
        ["incident_id"],
    )

    # =====================================================
    # 🔧 HSE INCIDENT INVESTIGATION MASTER HISTORY (ADD COLUMN)
    # =====================================================
    op.add_column(
        "hse_incident_investigation_master_history",
        sa.Column("incident_id", sa.Integer(), nullable=True)
    )

    # =====================================================
    # 🆕 CAPA REPORT (MAIN)
    # =====================================================
    op.create_table(
        "capa_report",
        sa.Column("capa_report_id", sa.Integer(), primary_key=True, autoincrement=True),

        sa.Column(
            "incident_id",
            sa.Integer(),
            sa.ForeignKey("incident_report.incident_id"),
            nullable=False,
        ),

        sa.Column("format_no", sa.String(50)),
        sa.Column("revision_date", sa.String(50)),
        sa.Column("report_no", sa.String(100)),

        sa.Column("department", sa.String(150)),
        sa.Column("start_date", sa.Date()),
        sa.Column("team_or_capa_study", sa.String(255)),
        sa.Column("planned_completion_date", sa.Date()),
        sa.Column("reference_no", sa.String(100)),

        sa.Column("problem_description", sa.Text()),

        sa.Column("correction_action", sa.Text()),
        sa.Column("correction_target_date", sa.Date()),
        sa.Column("correction_actual_date", sa.Date()),

        sa.Column("root_cause_analysis", sa.Text()),

        sa.Column("corrective_action", sa.Text()),
        sa.Column("corrective_target_date", sa.Date()),
        sa.Column("corrective_actual_date", sa.Date()),

        sa.Column("preventive_action", sa.Text()),
        sa.Column("preventive_target_date", sa.Date()),
        sa.Column("preventive_actual_date", sa.Date()),

        sa.Column("evidence_file_name", sa.String(255)),
        sa.Column("evidence_file_path", sa.String(500)),
        sa.Column("evidence_file_type", sa.String(50)),
        sa.Column("evidence_uploaded_at", sa.DateTime()),

        sa.Column("prepared_by_name", sa.String(150)),
        sa.Column("prepared_by_designation", sa.String(150)),
        sa.Column("approved_by_name", sa.String(150)),
        sa.Column("approved_by_designation", sa.String(150)),

        sa.Column("remarks", sa.Text()),
        sa.Column("status", sa.String(50), server_default="Draft"),

        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )

    # =====================================================
    # 🆕 CAPA DOCUMENT CHANGE
    # =====================================================
    op.create_table(
        "capa_document_change",
        sa.Column("capa_doc_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "capa_id",
            sa.Integer(),
            sa.ForeignKey("capa_report.capa_report_id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("document_code", sa.String(100)),
        sa.Column("changes_in_brief", sa.String(500)),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    # =====================================================
    # 🆕 CAPA DOCUMENT CHANGE HISTORY
    # =====================================================
    op.create_table(
        "capa_document_change_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("capa_id", sa.Integer()),
        sa.Column("capa_doc_id", sa.Integer()),
        sa.Column("document_code", sa.String(100)),
        sa.Column("changes_in_brief", sa.String(500)),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    # =====================================================
    # 🆕 CAPA REPORT HISTORY
    # =====================================================
    op.create_table(
        "capa_report_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("capa_report_id", sa.Integer()),
        sa.Column("incident_id", sa.Integer()),

        sa.Column("format_no", sa.String(50)),
        sa.Column("revision_date", sa.String(50)),
        sa.Column("report_no", sa.String(100)),

        sa.Column("department", sa.String(150)),
        sa.Column("start_date", sa.Date()),
        sa.Column("team_or_capa_study", sa.String(255)),
        sa.Column("planned_completion_date", sa.Date()),
        sa.Column("reference_no", sa.String(100)),

        sa.Column("problem_description", sa.Text()),

        sa.Column("correction_action", sa.Text()),
        sa.Column("correction_target_date", sa.Date()),
        sa.Column("correction_actual_date", sa.Date()),

        sa.Column("root_cause_analysis", sa.Text()),

        sa.Column("corrective_action", sa.Text()),
        sa.Column("corrective_target_date", sa.Date()),
        sa.Column("corrective_actual_date", sa.Date()),

        sa.Column("preventive_action", sa.Text()),
        sa.Column("preventive_target_date", sa.Date()),
        sa.Column("preventive_actual_date", sa.Date()),

        sa.Column("evidence_file_name", sa.String(255)),
        sa.Column("evidence_file_path", sa.String(500)),
        sa.Column("evidence_file_type", sa.String(50)),
        sa.Column("evidence_uploaded_at", sa.DateTime()),

        sa.Column("prepared_by_name", sa.String(150)),
        sa.Column("prepared_by_designation", sa.String(150)),
        sa.Column("approved_by_name", sa.String(150)),
        sa.Column("approved_by_designation", sa.String(150)),

        sa.Column("remarks", sa.Text()),
        sa.Column("status", sa.String(50)),

        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )


def downgrade():

    # CAPA tables
    op.drop_table("capa_report_history")
    op.drop_table("capa_document_change_history")
    op.drop_table("capa_document_change")
    op.drop_table("capa_report")

    # HSE columns rollback
    op.drop_constraint(
        "fk_hse_investigation_incident",
        "hse_incident_investigation_master",
        type_="foreignkey",
    )

    op.drop_column("hse_incident_investigation_master", "incident_id")
    op.drop_column("hse_incident_investigation_master_history", "incident_id")