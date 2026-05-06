"""create hse incident investigation modules

Revision ID: 5dc74e8279b8
Revises: 67931d3c3b2e
Create Date: 2026-02-02 12:54:57.322802

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5dc74e8279b8'
down_revision: Union[str, Sequence[str], None] = '67931d3c3b2e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():

    # =====================================================
    # MASTER TABLE
    # =====================================================
    op.create_table(
        "hse_incident_investigation_master",
        sa.Column("hiim_id", sa.Integer(), primary_key=True, autoincrement=True),

        sa.Column("incident_reference_no", sa.String(100)),
        sa.Column("report_number", sa.String(100)),

        sa.Column("incident_date", sa.Date()),
        sa.Column("incident_time", sa.Time()),
        sa.Column("reporting_date", sa.Date()),

        sa.Column("location_details", sa.String(255)),
        sa.Column("pipeline_name_section", sa.String(255)),
        sa.Column("reported_by", sa.String(150)),

        sa.Column("is_leak", sa.Boolean()),
        sa.Column("is_spill", sa.Boolean()),
        sa.Column("is_fire", sa.Boolean()),
        sa.Column("is_explosion", sa.Boolean()),
        sa.Column("is_injury", sa.Boolean()),
        sa.Column("is_near_miss", sa.Boolean()),
        sa.Column("is_other", sa.Boolean()),

        sa.Column("severity_major", sa.Boolean()),
        sa.Column("severity_minor", sa.Boolean()),
        sa.Column("severity_near_miss", sa.Boolean()),
        sa.Column("severity_unsafe_act", sa.Boolean()),
        sa.Column("severity_unsafe_condition", sa.Boolean()),
        sa.Column("severity_high_potential_near_miss", sa.Boolean()),

        sa.Column("impact_on_people", sa.Text()),
        sa.Column("impact_on_asset", sa.Text()),
        sa.Column("environmental_impact", sa.Text()),
        sa.Column("business_interruption", sa.Text()),

        sa.Column("immediate_action_taken", sa.Text()),
        sa.Column("statutory_management_intimation", sa.Text()),

        sa.Column("incident_description", sa.Text()),
        sa.Column("site_observations_evidence", sa.Text()),

        sa.Column("immediate_causes", sa.Text()),
        sa.Column("underlying_causes", sa.Text()),
        sa.Column("root_causes", sa.Text()),

        sa.Column("rca_tool_used", sa.String(50)),

        sa.Column("learning_recommendations", sa.Text()),
        sa.Column("verification_closure", sa.Text()),

        sa.Column("annexure_files", sa.Text()),

        sa.Column("remarks_md", sa.Text()),
        sa.Column("remarks_hse_head", sa.Text()),
        sa.Column("remarks_station_incharge", sa.Text()),

        sa.Column("allotted_to_name", sa.String(150)),
        sa.Column("allotted_to_designation", sa.String(150)),

        sa.Column("created_by", sa.String(100)),
        sa.Column("updated_by", sa.String(100)),

        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    # =====================================================
    # MASTER HISTORY
    # =====================================================
    op.create_table(
        "hse_incident_investigation_master_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("hiim_id", sa.Integer()),

        sa.Column("incident_reference_no", sa.String(100)),
        sa.Column("report_number", sa.String(100)),

        sa.Column("incident_date", sa.Date()),
        sa.Column("incident_time", sa.Time()),
        sa.Column("reporting_date", sa.Date()),

        sa.Column("location_details", sa.String(255)),
        sa.Column("pipeline_name_section", sa.String(255)),
        sa.Column("reported_by", sa.String(150)),

        sa.Column("is_leak", sa.Boolean()),
        sa.Column("is_spill", sa.Boolean()),
        sa.Column("is_fire", sa.Boolean()),
        sa.Column("is_explosion", sa.Boolean()),
        sa.Column("is_injury", sa.Boolean()),
        sa.Column("is_near_miss", sa.Boolean()),
        sa.Column("is_other", sa.Boolean()),

        sa.Column("severity_major", sa.Boolean()),
        sa.Column("severity_minor", sa.Boolean()),
        sa.Column("severity_near_miss", sa.Boolean()),
        sa.Column("severity_unsafe_act", sa.Boolean()),
        sa.Column("severity_unsafe_condition", sa.Boolean()),
        sa.Column("severity_high_potential_near_miss", sa.Boolean()),

        sa.Column("impact_on_people", sa.Text()),
        sa.Column("impact_on_asset", sa.Text()),
        sa.Column("environmental_impact", sa.Text()),
        sa.Column("business_interruption", sa.Text()),

        sa.Column("immediate_action_taken", sa.Text()),
        sa.Column("statutory_management_intimation", sa.Text()),

        sa.Column("incident_description", sa.Text()),
        sa.Column("site_observations_evidence", sa.Text()),

        sa.Column("immediate_causes", sa.Text()),
        sa.Column("underlying_causes", sa.Text()),
        sa.Column("root_causes", sa.Text()),

        sa.Column("rca_tool_used", sa.String(50)),

        sa.Column("learning_recommendations", sa.Text()),
        sa.Column("verification_closure", sa.Text()),

        sa.Column("annexure_files", sa.Text()),

        sa.Column("remarks_md", sa.Text()),
        sa.Column("remarks_hse_head", sa.Text()),
        sa.Column("remarks_station_incharge", sa.Text()),

        sa.Column("allotted_to_name", sa.String(150)),
        sa.Column("allotted_to_designation", sa.String(150)),

        sa.Column("created_by", sa.String(100)),
        sa.Column("updated_by", sa.String(100)),

        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    # =====================================================
    # RCA – 5 WHY
    # =====================================================
    op.create_table(
        "hse_incident_rca_5why",
        sa.Column("rca_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "incident_id",
            sa.Integer(),
            sa.ForeignKey("hse_incident_investigation_master.hiim_id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("why1", sa.Text()),
        sa.Column("why2", sa.Text()),
        sa.Column("why3", sa.Text()),
        sa.Column("why4", sa.Text()),
        sa.Column("why5_root_cause", sa.Text()),
    )

    op.create_table(
        "hse_incident_rca_5why_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("rca_id", sa.Integer()),
        sa.Column("incident_id", sa.Integer()),
        sa.Column("why1", sa.Text()),
        sa.Column("why2", sa.Text()),
        sa.Column("why3", sa.Text()),
        sa.Column("why4", sa.Text()),
        sa.Column("why5_root_cause", sa.Text()),
    )

    # =====================================================
    # INVESTIGATION TEAM
    # =====================================================
    op.create_table(
        "hse_incident_investigation_team",
        sa.Column("invest_team_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "incident_id",
            sa.Integer(),
            sa.ForeignKey("hse_incident_investigation_master.hiim_id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("sl_no", sa.Integer()),
        sa.Column("name", sa.String(150)),
        sa.Column("designation", sa.String(150)),
        sa.Column("role", sa.String(50)),
        sa.Column("is_acknowledged", sa.Boolean()),
    )

    op.create_table(
        "hse_incident_investigation_team_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("invest_team_id", sa.Integer()),
        sa.Column("incident_id", sa.Integer()),
        sa.Column("sl_no", sa.Integer()),
        sa.Column("name", sa.String(150)),
        sa.Column("designation", sa.String(150)),
        sa.Column("role", sa.String(50)),
        sa.Column("is_acknowledged", sa.Boolean()),
    )


def downgrade():
    op.drop_table("hse_incident_investigation_team_history")
    op.drop_table("hse_incident_investigation_team")
    op.drop_table("hse_incident_rca_5why_history")
    op.drop_table("hse_incident_rca_5why")
    op.drop_table("hse_incident_investigation_master_history")
    op.drop_table("hse_incident_investigation_master")