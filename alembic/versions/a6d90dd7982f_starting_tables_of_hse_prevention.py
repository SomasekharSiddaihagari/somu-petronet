"""starting tables of hse prevention

Revision ID: a6d90dd7982f
Revises: 49cca6e67a93
Create Date: 2026-01-30 18:16:06.047466

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a6d90dd7982f'
down_revision: Union[str, Sequence[str], None] = '49cca6e67a93'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # =========================
    # incident_prevention
    # =========================
    op.create_table(
        'incident_prevention',
        sa.Column('ip_id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('incident_id', sa.Integer()),

        # COMMON
        sa.Column('category', sa.String(50)),
        sa.Column('status', sa.String(50)),
        sa.Column('was_incident_avoidable', sa.Boolean()),

        sa.Column('avoid_better_supervision', sa.Boolean()),
        sa.Column('avoid_imparting_training', sa.Boolean()),
        sa.Column('avoid_work_permit_system', sa.Boolean()),
        sa.Column('avoid_better_equipment', sa.Boolean()),
        sa.Column('avoid_maintenance_procedure', sa.Boolean()),
        sa.Column('avoid_other_information', sa.Boolean()),

        sa.Column('avoid_operating_procedure', sa.Boolean()),
        sa.Column('avoid_proper_planning_time', sa.Boolean()),
        sa.Column('avoid_ppe', sa.Boolean()),
        sa.Column('avoid_management_control', sa.Boolean()),
        sa.Column('avoid_inspection_testing', sa.Boolean()),

        # MINOR
        sa.Column('minor_prepared_by_name', sa.String(150)),
        sa.Column('minor_prepared_by_designation', sa.String(150)),

        sa.Column('minor_recommendations', sa.Text()),
        sa.Column('minor_engineer_corrective_actions_taken', sa.Text()),
        sa.Column('minor_prepared_by_corrective_action', sa.Text()),
        sa.Column('minor_corrective_actions', sa.Text()),

        sa.Column('minor_prepared_by_remarks', sa.Text()),
        sa.Column('minor_preventive_action_taken', sa.Text()),

        sa.Column('minor_allotted_engineer_name', sa.String(150)),
        sa.Column('minor_allotted_engineer_designation', sa.String(150)),

        sa.Column('minor_approved_by_name', sa.String(150)),
        sa.Column('minor_approved_by_station_incharge', sa.String(150)),
        sa.Column('minor_approved_by_remarks', sa.Text()),

        sa.Column('minor_evidence_document_path', sa.String(255)),

        # MAJOR
        sa.Column('major_prepared_by_name', sa.String(150)),
        sa.Column('major_prepared_by_designation', sa.String(150)),

        sa.Column('major_immediate_actions_taken', sa.Text()),
        sa.Column('major_recommendations', sa.Text()),

        sa.Column('major_prepared_by_remarks_si', sa.Text()),
        sa.Column('major_hse_head_remarks', sa.Text()),

        sa.Column('major_evidence_document_path', sa.String(255)),

        # SYSTEM
        sa.Column('created_by', sa.String(100)),
        sa.Column('updated_by', sa.String(100)),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime()),
    )

    # =========================
    # incident_prevention_history
    # =========================
    op.create_table(
        'incident_prevention_history',
        sa.Column('history_id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('ip_id', sa.Integer()),
        sa.Column('incident_id', sa.Integer()),

        # COMMON
        sa.Column('category', sa.String(50)),
        sa.Column('status', sa.String(50)),
        sa.Column('was_incident_avoidable', sa.Boolean()),

        sa.Column('avoid_better_supervision', sa.Boolean()),
        sa.Column('avoid_imparting_training', sa.Boolean()),
        sa.Column('avoid_work_permit_system', sa.Boolean()),
        sa.Column('avoid_better_equipment', sa.Boolean()),
        sa.Column('avoid_maintenance_procedure', sa.Boolean()),
        sa.Column('avoid_other_information', sa.Boolean()),

        sa.Column('avoid_operating_procedure', sa.Boolean()),
        sa.Column('avoid_proper_planning_time', sa.Boolean()),
        sa.Column('avoid_ppe', sa.Boolean()),
        sa.Column('avoid_management_control', sa.Boolean()),
        sa.Column('avoid_inspection_testing', sa.Boolean()),

        # MINOR
        sa.Column('minor_prepared_by_name', sa.String(150)),
        sa.Column('minor_prepared_by_designation', sa.String(150)),

        sa.Column('minor_recommendations', sa.Text()),
        sa.Column('minor_engineer_corrective_actions_taken', sa.Text()),
        sa.Column('minor_prepared_by_corrective_action', sa.Text()),
        sa.Column('minor_corrective_actions', sa.Text()),

        sa.Column('minor_prepared_by_remarks', sa.Text()),
        sa.Column('minor_preventive_action_taken', sa.Text()),

        sa.Column('minor_allotted_engineer_name', sa.String(150)),
        sa.Column('minor_allotted_engineer_designation', sa.String(150)),

        sa.Column('minor_approved_by_name', sa.String(150)),
        sa.Column('minor_approved_by_station_incharge', sa.String(150)),
        sa.Column('minor_approved_by_remarks', sa.Text()),

        sa.Column('minor_evidence_document_path', sa.String(255)),

        # MAJOR
        sa.Column('major_prepared_by_name', sa.String(150)),
        sa.Column('major_prepared_by_designation', sa.String(150)),

        sa.Column('major_immediate_actions_taken', sa.Text()),
        sa.Column('major_recommendations', sa.Text()),

        sa.Column('major_prepared_by_remarks_si', sa.Text()),
        sa.Column('major_hse_head_remarks', sa.Text()),

        sa.Column('major_evidence_document_path', sa.String(255)),

        # SYSTEM
        sa.Column('created_by', sa.String(100)),
        sa.Column('updated_by', sa.String(100)),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime()),
    )


def downgrade():
    op.drop_table('incident_prevention_history')
    op.drop_table('incident_prevention')