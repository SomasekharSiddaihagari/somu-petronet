"""create height permit and history tables

Revision ID: 60c00e9f32ac
Revises: b5a0c0dc310b
Create Date: 2026-01-23 20:34:38.447668

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '60c00e9f32ac'
down_revision: Union[str, Sequence[str], None] = 'b5a0c0dc310b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    # =================================================
    # work_at_height_permit
    # =================================================
    op.create_table(
        'work_at_height_permit',
        sa.Column('whp_id', sa.Integer(), primary_key=True),
        sa.Column('serial_number', sa.String(150)),
        sa.Column('section_contractor_name', sa.String(255)),
        sa.Column('nature_of_work', sa.Text()),
        sa.Column('work_from_time', sa.Time()),
        sa.Column('work_from_date', sa.Date()),
        sa.Column('work_to_time', sa.Time()),
        sa.Column('work_to_date', sa.Date()),
        sa.Column('location', sa.String(255)),

        sa.Column('sc1_equipment_work_area_inspected', sa.String(20)),
        sa.Column('sc2_surrounding_area_checked', sa.String(20)),
        sa.Column('sc3_sewers_manholes_covered', sa.String(20)),
        sa.Column('sc4_scaffolds_ladders_checked', sa.String(20)),
        sa.Column('sc5_materials_fall_protected', sa.String(20)),
        sa.Column('sc6_isi_marked_belts_helmets', sa.String(20)),
        sa.Column('sc7_contractor_fit_for_height', sa.String(20)),
        sa.Column('sc8_instructions_given', sa.String(20)),
        sa.Column('sc9_proper_illumination', sa.String(20)),
        sa.Column('sc10_adequate_platform_space', sa.String(20)),
        sa.Column('sc11_proper_exit_means', sa.String(20)),
        sa.Column('sc12_precautionary_tags_boards', sa.String(20)),
        sa.Column('sc13_portable_equipment_earthed', sa.String(20)),
        sa.Column('sc14_elcb_switches_provided', sa.String(20)),
        sa.Column('sc15_standby_supervision_provided', sa.String(20)),
        sa.Column('sc16_workers_trained_safety_belts', sa.String(20)),
        sa.Column('sc17_operations_incharge_informed', sa.String(20)),
        sa.Column('sc18_area_cordoned_off', sa.String(20)),
        sa.Column('sc19_precautions_against_public_traffic', sa.String(20)),
        sa.Column('sc20_fire_extinguisher_provided', sa.String(20)),

        sa.Column('special_instructions', sa.Text()),
        sa.Column('additional_remarks', sa.Text()),

        sa.Column('issuer_designation', sa.String(150)),
        sa.Column('issuer_name', sa.String(150)),
        sa.Column('issuer_signature', sa.String(255)),

        sa.Column('receiver_role', sa.String(150)),
        sa.Column('receiver_name', sa.String(150)),
        sa.Column('receiver_signature', sa.String(255)),

        sa.Column('electrical_isolation_required', sa.Boolean()),
        sa.Column('electrical_energization_required', sa.Boolean()),
        sa.Column('toolbox_talk_required', sa.Boolean()),

        sa.Column('renewal_from_date', sa.Date()),
        sa.Column('renewal_from_time', sa.Time()),
        sa.Column('renewal_to_date', sa.Date()),
        sa.Column('renewal_to_time', sa.Time()),

        sa.Column('renewal_issuer_name', sa.String(150)),
        sa.Column('renewal_issuer_designation', sa.String(150)),
        sa.Column('renewal_issuer_signature', sa.String(255)),

        sa.Column('renewal_receiver_name', sa.String(150)),
        sa.Column('renewal_receiver_designation', sa.String(150)),
        sa.Column('renewal_receiver_signature', sa.String(255)),

        sa.Column('renewal_toolbox_talk', sa.Boolean()),

        sa.Column('closure_issuer_designation', sa.String(150)),
        sa.Column('closure_issuer_name', sa.String(150)),
        sa.Column('closure_issuer_signature', sa.String(255)),

        sa.Column('closure_receiver_role', sa.String(150)),
        sa.Column('closure_receiver_name', sa.String(150)),
        sa.Column('closure_receiver_signature', sa.String(255)),

        sa.Column('job_completion_time', sa.Time()),
        sa.Column('job_completion_date', sa.Date()),
        sa.Column('work_status', sa.Text()),

        sa.Column('status', sa.String(50)),
        sa.Column('created_by', sa.String(100)),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime()),
    )

    # =================================================
    # work_at_height_permit_history
    # =================================================
    op.create_table(
        'work_at_height_permit_history',
        sa.Column('history_id', sa.Integer(), primary_key=True),
        sa.Column('whp_id', sa.Integer()),
        sa.Column('serial_number', sa.String(150)),
        sa.Column('section_contractor_name', sa.String(255)),
        sa.Column('nature_of_work', sa.Text()),
        sa.Column('work_from_time', sa.Time()),
        sa.Column('work_from_date', sa.Date()),
        sa.Column('work_to_time', sa.Time()),
        sa.Column('work_to_date', sa.Date()),
        sa.Column('location', sa.String(255)),

        sa.Column('special_instructions', sa.Text()),
        sa.Column('additional_remarks', sa.Text()),

        sa.Column('issuer_designation', sa.String(150)),
        sa.Column('issuer_name', sa.String(150)),
        sa.Column('issuer_signature', sa.String(255)),

        sa.Column('receiver_role', sa.String(150)),
        sa.Column('receiver_name', sa.String(150)),
        sa.Column('receiver_signature', sa.String(255)),

        sa.Column('electrical_isolation_required', sa.Boolean()),
        sa.Column('electrical_energization_required', sa.Boolean()),
        sa.Column('toolbox_talk_required', sa.Boolean()),

        sa.Column('status', sa.String(50)),
        sa.Column('created_by', sa.String(100)),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime()),
    )

    # =================================================
    # work_at_height_toolbox_talk
    # =================================================
    op.create_table(
        'work_at_height_toolbox_talk',
        sa.Column('whtt_id', sa.Integer(), primary_key=True),
        sa.Column('work_at_height_permit_id', sa.Integer()),
        sa.Column('cross_reference_of_other_permit', sa.String(150)),
        sa.Column('work_clearance_time', sa.Time()),
        sa.Column('work_clearance_date', sa.Date()),
        sa.Column('contractor_engineer_name', sa.String(150)),
        sa.Column('work_installation_unit_facility_name', sa.String(255)),
        sa.Column('tbt_delivered_by', sa.String(150)),
        sa.Column('contract_supervisor_name', sa.String(150)),
        sa.Column('topics_issues_discussed', sa.Text()),
        sa.Column('other_points_raised', sa.Text()),
        sa.Column('created_by', sa.String(100)),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime()),
    )

    # =================================================
    # work_at_height_toolbox_talk_history
    # =================================================
    op.create_table(
        'work_at_height_toolbox_talk_history',
        sa.Column('history_id', sa.Integer(), primary_key=True),
        sa.Column('whtt_id', sa.Integer()),
        sa.Column('work_at_height_permit_id', sa.Integer()),
        sa.Column('cross_reference_of_other_permit', sa.String(150)),
        sa.Column('work_clearance_time', sa.Time()),
        sa.Column('work_clearance_date', sa.Date()),
        sa.Column('contractor_engineer_name', sa.String(150)),
        sa.Column('work_installation_unit_facility_name', sa.String(255)),
        sa.Column('tbt_delivered_by', sa.String(150)),
        sa.Column('contract_supervisor_name', sa.String(150)),
        sa.Column('topics_issues_discussed', sa.Text()),
        sa.Column('other_points_raised', sa.Text()),
        sa.Column('created_by', sa.String(100)),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime()),
    )

    # =================================================
    # work_at_height_toolbox_talk_participant
    # =================================================
    op.create_table(
        'work_at_height_toolbox_talk_participant',
        sa.Column('whttp_id', sa.Integer(), primary_key=True),
        sa.Column('toolbox_talk_id', sa.Integer()),
        sa.Column('participant_name', sa.String(150)),
        sa.Column('participant_signature', sa.String(255)),
        sa.Column('created_at', sa.DateTime()),
    )

    # =================================================
    # work_at_height_toolbox_talk_participant_history
    # =================================================
    op.create_table(
        'work_at_height_toolbox_talk_participant_history',
        sa.Column('history_id', sa.Integer(), primary_key=True),
        sa.Column('whttp_id', sa.Integer()),
        sa.Column('toolbox_talk_id', sa.Integer()),
        sa.Column('participant_name', sa.String(150)),
        sa.Column('participant_signature', sa.String(255)),
        sa.Column('created_at', sa.DateTime()),
    )

    # =================================================
    # work_at_height_electrical_isolation_permit
    # =================================================
    op.create_table(
        'work_at_height_electrical_isolation_permit',
        sa.Column('whpis_id', sa.Integer(), primary_key=True),
        sa.Column('whp_id', sa.Integer()),
        sa.Column('work_permit_number', sa.String(150)),
        sa.Column('work_clearance_time', sa.Time()),
        sa.Column('work_clearance_date', sa.Date()),
        sa.Column('cross_reference_of_other_permit', sa.String(150)),
        sa.Column('department_section_area', sa.String(255)),
        sa.Column('equipment_number_to_be_isolated', sa.String(255)),
        sa.Column('name_of_equipment_circuit', sa.String(255)),
        sa.Column('description_of_work', sa.Text()),
        sa.Column('issuer_name', sa.String(150)),
        sa.Column('issuer_designation', sa.String(150)),
        sa.Column('issuer_signature', sa.String(255)),
        sa.Column('created_by', sa.String(100)),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime()),
    )

    # =================================================
    # work_at_height_electrical_isolation_permit_history
    # =================================================
    op.create_table(
        'work_at_height_electrical_isolation_permit_history',
        sa.Column('history_id', sa.Integer(), primary_key=True),
        sa.Column('whp_id', sa.Integer()),
        sa.Column('work_permit_number', sa.String(150)),
        sa.Column('work_clearance_time', sa.Time()),
        sa.Column('work_clearance_date', sa.Date()),
        sa.Column('cross_reference_of_other_permit', sa.String(150)),
        sa.Column('department_section_area', sa.String(255)),
        sa.Column('equipment_number_to_be_isolated', sa.String(255)),
        sa.Column('name_of_equipment_circuit', sa.String(255)),
        sa.Column('description_of_work', sa.Text()),
        sa.Column('issuer_name', sa.String(150)),
        sa.Column('issuer_designation', sa.String(150)),
        sa.Column('issuer_signature', sa.String(255)),
        sa.Column('created_by', sa.String(100)),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime()),
    )

    # =================================================
    # work_at_height_electrical_energization_permit
    # =================================================
    op.create_table(
        'work_at_height_electrical_energization_permit',
        sa.Column('whpep_id', sa.Integer(), primary_key=True),
        sa.Column('whp_id', sa.Integer()),
        sa.Column('work_permit_number', sa.String(150)),
        sa.Column('work_clearance_time', sa.Time()),
        sa.Column('work_clearance_date', sa.Date()),
        sa.Column('name_of_equipment_circuit', sa.String(255)),
        sa.Column('department_section_area', sa.String(255)),
        sa.Column('equipment_number_to_be_energized', sa.String(255)),
        sa.Column('cross_reference_of_other_permit', sa.String(150)),
        sa.Column('issuer_name', sa.String(150)),
        sa.Column('issuer_designation', sa.String(150)),
        sa.Column('issuer_signature', sa.String(255)),
        sa.Column('created_by', sa.String(100)),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime()),
    )

    # =================================================
    # work_at_height_electrical_energization_permit_history
    # =================================================
    op.create_table(
        'work_at_height_electrical_energization_permit_history',
        sa.Column('history_id', sa.Integer(), primary_key=True),
        sa.Column('whpep_id', sa.Integer()),
        sa.Column('whp_id', sa.Integer()),
        sa.Column('work_permit_number', sa.String(150)),
        sa.Column('work_clearance_time', sa.Time()),
        sa.Column('work_clearance_date', sa.Date()),
        sa.Column('name_of_equipment_circuit', sa.String(255)),
        sa.Column('department_section_area', sa.String(255)),
        sa.Column('equipment_number_to_be_energized', sa.String(255)),
        sa.Column('cross_reference_of_other_permit', sa.String(150)),
        sa.Column('issuer_name', sa.String(150)),
        sa.Column('issuer_designation', sa.String(150)),
        sa.Column('issuer_signature', sa.String(255)),
        sa.Column('created_by', sa.String(100)),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime()),
    )


def downgrade():
    op.drop_table('work_at_height_electrical_energization_permit_history')
    op.drop_table('work_at_height_electrical_energization_permit')
    op.drop_table('work_at_height_electrical_isolation_permit_history')
    op.drop_table('work_at_height_electrical_isolation_permit')
    op.drop_table('work_at_height_toolbox_talk_participant_history')
    op.drop_table('work_at_height_toolbox_talk_participant')
    op.drop_table('work_at_height_toolbox_talk_history')
    op.drop_table('work_at_height_toolbox_talk')
    op.drop_table('work_at_height_permit_history')
    op.drop_table('work_at_height_permit')