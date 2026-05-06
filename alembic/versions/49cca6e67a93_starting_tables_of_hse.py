"""starting tables of hse

Revision ID: 49cca6e67a93
Revises: 986b02ff45c5
Create Date: 2026-01-30 17:00:10.888104

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '49cca6e67a93'
down_revision: Union[str, Sequence[str], None] = '986b02ff45c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # =========================
    # incident_report
    # =========================
    op.create_table(
        'incident_report',
        sa.Column('incident_id', sa.Integer(), primary_key=True, autoincrement=True),

        sa.Column('organisation', sa.String(150)),
        sa.Column('category', sa.String(50)),
        sa.Column('sector', sa.String(150)),
        sa.Column('location', sa.String(255)),
        sa.Column('incident_no_during_year', sa.String(100)),

        sa.Column('date_of_incident', sa.Date()),
        sa.Column('time_of_incident', sa.Time()),

        sa.Column('incident_type', sa.String(100)),
        sa.Column('fire_incident', sa.String(100)),

        sa.Column('report_type', sa.String(50)),
        sa.Column('duration_of_fire', sa.String(50)),

        sa.Column('loss_of_life_injury', sa.Boolean()),
        sa.Column('electrocution', sa.Boolean()),
        sa.Column('slip_trip', sa.Boolean()),
        sa.Column('fire', sa.Boolean()),
        sa.Column('fall_from_height', sa.Boolean()),
        sa.Column('leak_spill', sa.Boolean()),
        sa.Column('explosion', sa.Boolean()),
        sa.Column('inhalation_of_gas', sa.Boolean()),
        sa.Column('blowout', sa.Boolean()),
        sa.Column('driving', sa.Boolean()),

        sa.Column('others', sa.Boolean()),
        sa.Column('others_text', sa.String(255)),

        sa.Column('incident_location_detail', sa.Text()),

        sa.Column('plant_shutdown', sa.Boolean()),

        sa.Column('status', sa.String(50)),
        sa.Column('created_by', sa.String(100)),
        sa.Column('updated_by', sa.String(100)),

        sa.Column('created_at', sa.Date()),
        sa.Column('updated_at', sa.Date()),
    )

    # =========================
    # incident_report_history
    # =========================
    op.create_table(
        'incident_report_history',
        sa.Column('history_id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('incident_id', sa.Integer()),

        sa.Column('organisation', sa.String(150)),
        sa.Column('category', sa.String(50)),
        sa.Column('sector', sa.String(150)),
        sa.Column('location', sa.String(255)),
        sa.Column('incident_no_during_year', sa.String(100)),

        sa.Column('date_of_incident', sa.Date()),
        sa.Column('time_of_incident', sa.Time()),

        sa.Column('incident_type', sa.String(100)),
        sa.Column('fire_incident', sa.String(100)),

        sa.Column('report_type', sa.String(50)),
        sa.Column('duration_of_fire', sa.String(50)),

        sa.Column('loss_of_life_injury', sa.Boolean()),
        sa.Column('electrocution', sa.Boolean()),
        sa.Column('slip_trip', sa.Boolean()),
        sa.Column('fire', sa.Boolean()),
        sa.Column('fall_from_height', sa.Boolean()),
        sa.Column('leak_spill', sa.Boolean()),
        sa.Column('explosion', sa.Boolean()),
        sa.Column('inhalation_of_gas', sa.Boolean()),
        sa.Column('blowout', sa.Boolean()),
        sa.Column('driving', sa.Boolean()),

        sa.Column('others', sa.Boolean()),
        sa.Column('others_text', sa.String(255)),

        sa.Column('incident_location_detail', sa.Text()),
        sa.Column('plant_shutdown', sa.Boolean()),

        sa.Column('status', sa.String(50)),
        sa.Column('created_by', sa.String(100)),
        sa.Column('updated_by', sa.String(100)),

        sa.Column('created_at', sa.Date()),
        sa.Column('updated_at', sa.Date()),
    )

    # =========================
    # incident_impact_assessment
    # =========================
    op.create_table(
        'incident_impact_assessment',
        sa.Column('impact_id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('incident_id', sa.Integer()),

        sa.Column('fatalities_employees', sa.Integer()),
        sa.Column('fatalities_contractor', sa.Integer()),
        sa.Column('fatalities_others', sa.Integer()),

        sa.Column('injuries_employees', sa.Integer()),
        sa.Column('injuries_contractor', sa.Integer()),
        sa.Column('injuries_others', sa.Integer()),

        sa.Column('man_hours_lost_employees', sa.Integer()),
        sa.Column('man_hours_lost_contractor', sa.Integer()),
        sa.Column('man_hours_lost_others', sa.Integer()),

        sa.Column('direct_loss_details', sa.Text()),
        sa.Column('indirect_loss_details', sa.Text()),

        sa.Column('facility_status', sa.String(50)),
        sa.Column('brief_incident_description', sa.Text()),
        sa.Column('similar_incident_past', sa.Text()),

        sa.Column('status', sa.String(50)),
        sa.Column('created_by', sa.String(100)),
        sa.Column('updated_by', sa.String(100)),

        sa.Column('created_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime()),
    )

    # =========================
    # incident_impact_assessment_history
    # =========================
    op.create_table(
        'incident_impact_assessment_history',
        sa.Column('history_id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('impact_id', sa.Integer()),
        sa.Column('incident_id', sa.Integer()),

        sa.Column('fatalities_employees', sa.Integer()),
        sa.Column('fatalities_contractor', sa.Integer()),
        sa.Column('fatalities_others', sa.Integer()),

        sa.Column('injuries_employees', sa.Integer()),
        sa.Column('injuries_contractor', sa.Integer()),
        sa.Column('injuries_others', sa.Integer()),

        sa.Column('man_hours_lost_employees', sa.Integer()),
        sa.Column('man_hours_lost_contractor', sa.Integer()),
        sa.Column('man_hours_lost_others', sa.Integer()),

        sa.Column('direct_loss_details', sa.Text()),
        sa.Column('indirect_loss_details', sa.Text()),

        sa.Column('facility_status', sa.String(50)),
        sa.Column('brief_incident_description', sa.Text()),
        sa.Column('similar_incident_past', sa.Text()),

        sa.Column('status', sa.String(50)),
        sa.Column('created_by', sa.String(100)),
        sa.Column('updated_by', sa.String(100)),

        sa.Column('created_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime()),
    )

    # =========================
    # incident_cause_analysis
    # =========================
    op.create_table(
        'incident_cause_analysis',
        sa.Column('cause_id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('incident_id', sa.Integer()),

        # All cause, leak & ignition boolean fields
        sa.Column('cause_deviation_from_procedure', sa.Boolean()),
        sa.Column('cause_lack_of_job_knowledge', sa.Boolean()),
        sa.Column('cause_lack_of_supervision', sa.Boolean()),
        sa.Column('cause_improper_inspection', sa.Boolean()),
        sa.Column('cause_improper_maintenance', sa.Boolean()),
        sa.Column('cause_improper_material_handling', sa.Boolean()),
        sa.Column('cause_negligent_driving', sa.Boolean()),
        sa.Column('cause_not_using_ppe', sa.Boolean()),
        sa.Column('cause_equipment_failure', sa.Boolean()),
        sa.Column('cause_poor_design_layout', sa.Boolean()),
        sa.Column('cause_inadequate_facility', sa.Boolean()),
        sa.Column('cause_poor_house_keeping', sa.Boolean()),
        sa.Column('cause_natural_calamity', sa.Boolean()),
        sa.Column('cause_pilferage_sabotage', sa.Boolean()),

        sa.Column('leak_weld_from_equipment_lines', sa.Boolean()),
        sa.Column('leak_from_flange_gland', sa.Boolean()),
        sa.Column('leak_from_rotary_equipment', sa.Boolean()),
        sa.Column('leak_metallurgical_failure', sa.Boolean()),
        sa.Column('leak_due_to_improper_operation', sa.Boolean()),
        sa.Column('leak_due_to_improper_maintenance', sa.Boolean()),
        sa.Column('leak_normal_operation_venting_draining', sa.Boolean()),
        sa.Column('leak_any_other', sa.Boolean()),

        sa.Column('ignition_near_to_hot_work', sa.Boolean()),
        sa.Column('ignition_near_to_furnace_flare', sa.Boolean()),
        sa.Column('ignition_auto_ignition', sa.Boolean()),
        sa.Column('ignition_loose_electrical_connection', sa.Boolean()),
        sa.Column('ignition_near_to_hot_surface', sa.Boolean()),
        sa.Column('ignition_static_electricity', sa.Boolean()),
        sa.Column('ignition_hammering_fall_of_object', sa.Boolean()),
        sa.Column('ignition_heat_due_to_friction', sa.Boolean()),
        sa.Column('ignition_lightning', sa.Boolean()),
        sa.Column('ignition_any_other_pyrophoric', sa.Boolean()),

        sa.Column('status', sa.String(50)),
        sa.Column('created_by', sa.String(100)),
        sa.Column('updated_by', sa.String(100)),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime()),
    )

    # =========================
    # incident_cause_analysis_history
    # =========================
    op.create_table(
        'incident_cause_analysis_history',
        sa.Column('history_id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('cause_id', sa.Integer()),
        sa.Column('incident_id', sa.Integer()),

        # same boolean fields as above
        sa.Column('cause_deviation_from_procedure', sa.Boolean()),
        sa.Column('cause_lack_of_job_knowledge', sa.Boolean()),
        sa.Column('cause_lack_of_supervision', sa.Boolean()),
        sa.Column('cause_improper_inspection', sa.Boolean()),
        sa.Column('cause_improper_maintenance', sa.Boolean()),
        sa.Column('cause_improper_material_handling', sa.Boolean()),
        sa.Column('cause_negligent_driving', sa.Boolean()),
        sa.Column('cause_not_using_ppe', sa.Boolean()),
        sa.Column('cause_equipment_failure', sa.Boolean()),
        sa.Column('cause_poor_design_layout', sa.Boolean()),
        sa.Column('cause_inadequate_facility', sa.Boolean()),
        sa.Column('cause_poor_house_keeping', sa.Boolean()),
        sa.Column('cause_natural_calamity', sa.Boolean()),
        sa.Column('cause_pilferage_sabotage', sa.Boolean()),

        sa.Column('leak_weld_from_equipment_lines', sa.Boolean()),
        sa.Column('leak_from_flange_gland', sa.Boolean()),
        sa.Column('leak_from_rotary_equipment', sa.Boolean()),
        sa.Column('leak_metallurgical_failure', sa.Boolean()),
        sa.Column('leak_due_to_improper_operation', sa.Boolean()),
        sa.Column('leak_due_to_improper_maintenance', sa.Boolean()),
        sa.Column('leak_normal_operation_venting_draining', sa.Boolean()),
        sa.Column('leak_any_other', sa.Boolean()),

        sa.Column('ignition_near_to_hot_work', sa.Boolean()),
        sa.Column('ignition_near_to_furnace_flare', sa.Boolean()),
        sa.Column('ignition_auto_ignition', sa.Boolean()),
        sa.Column('ignition_loose_electrical_connection', sa.Boolean()),
        sa.Column('ignition_near_to_hot_surface', sa.Boolean()),
        sa.Column('ignition_static_electricity', sa.Boolean()),
        sa.Column('ignition_hammering_fall_of_object', sa.Boolean()),
        sa.Column('ignition_heat_due_to_friction', sa.Boolean()),
        sa.Column('ignition_lightning', sa.Boolean()),
        sa.Column('ignition_any_other_pyrophoric', sa.Boolean()),

        sa.Column('status', sa.String(50)),
        sa.Column('created_by', sa.String(100)),
        sa.Column('updated_by', sa.String(100)),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime()),
    )


def downgrade():
    op.drop_table('incident_cause_analysis_history')
    op.drop_table('incident_cause_analysis')
    op.drop_table('incident_impact_assessment_history')
    op.drop_table('incident_impact_assessment')
    op.drop_table('incident_report_history')
    op.drop_table('incident_report')