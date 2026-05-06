"""create composite permit and history tables

Revision ID: b5a0c0dc310b
Revises: 8bb28445e0e0
Create Date: 2026-01-23 20:01:52.018734

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b5a0c0dc310b'
down_revision: Union[str, Sequence[str], None] = '8bb28445e0e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # ===============================
    # composite_work_permit
    # ===============================
    op.create_table(
        'composite_work_permit',
        sa.Column('cwp_id', sa.Integer(), primary_key=True),
        sa.Column('serial_number', sa.String(100)),
        sa.Column('location', sa.String(255)),
        sa.Column('issued_to', sa.String(255)),
        sa.Column('description_of_work', sa.Text()),
        sa.Column('work_from_time', sa.Time()),
        sa.Column('work_from_date', sa.Date()),
        sa.Column('work_to_time', sa.Time()),
        sa.Column('work_to_date', sa.Date()),
        sa.Column('jsa_ref_no', sa.String(100)),
        sa.Column('cross_reference_permits', sa.String(100)),
        sa.Column('isolation_certificate_ref', sa.String(100)),
        sa.Column('a1_equipment_area_inspected', sa.String(20)),
        sa.Column('a2_surrounding_area_checked', sa.String(20)),
        sa.Column('a3_sewers_manholes_covered', sa.String(20)),
        sa.Column('a4_hazards_considered', sa.String(20)),
        sa.Column('a5_equipment_drained', sa.String(20)),
        sa.Column('a6_equipment_steamed_purged', sa.String(20)),
        sa.Column('a7_equipment_blinded_isolated', sa.String(20)),
        sa.Column('a8_equipment_water_flushed', sa.String(20)),
        sa.Column('a9_iron_sulphide_removed', sa.String(20)),
        sa.Column('a10_equipment_electrically_isolated', sa.String(20)),
        sa.Column('a11_gas_test', sa.String(20)),
        sa.Column('a12_fire_extinguisher_provided', sa.String(20)),
        sa.Column('a13_area_cordoned', sa.String(20)),
        sa.Column('a14_ventilation_lighting', sa.String(20)),
        sa.Column('b1_escape_provided', sa.String(20)),
        sa.Column('b2_standby_personnel', sa.String(20)),
        sa.Column('b3_check_oil_gas_trapped', sa.String(20)),
        sa.Column('b4_shield_against_spark', sa.String(20)),
        sa.Column('b5_portable_equipment_grounded', sa.String(20)),
        sa.Column('b6_standby_for_confined_space', sa.String(20)),
        sa.Column('c1_peso_spark_elimination', sa.String(20)),
        sa.Column('d1_excavation_clearance_obtained', sa.String(20)),
        sa.Column('remarks_hazards', sa.Text()),
        sa.Column('additional_requirements_precautions', sa.Text()),
        sa.Column('issuer_name', sa.String(150)),
        sa.Column('issuer_designation', sa.String(150)),
        sa.Column('issuer_signature', sa.String(255)),
        sa.Column('receiver_role', sa.String(150)),
        sa.Column('receiver_name', sa.String(150)),
        sa.Column('receiver_signature', sa.String(255)),
        sa.Column('electrical_isolation_required', sa.Boolean()),
        sa.Column('electrical_energization_required', sa.Boolean()),
        sa.Column('toolbox_talk_completed', sa.Boolean()),
        sa.Column('gas_test_from_time', sa.Time()),
        sa.Column('gas_test_to_time', sa.Time()),
        sa.Column('gas_test_from_date', sa.Date()),
        sa.Column('gas_test_to_date', sa.Date()),
        sa.Column('gas_hcs_percent', sa.String(50)),
        sa.Column('gas_toxic_ppm', sa.String(50)),
        sa.Column('gas_o2_percent', sa.String(50)),
        sa.Column('gas_additional_precautions', sa.Text()),
        sa.Column('gas_issuer_name', sa.String(150)),
        sa.Column('gas_issuer_designation', sa.String(150)),
        sa.Column('gas_issuer_signature', sa.String(255)),
        sa.Column('gas_receiver_name', sa.String(150)),
        sa.Column('gas_receiver_designation', sa.String(150)),
        sa.Column('gas_receiver_signature', sa.String(255)),
        sa.Column('closure_issuer_name', sa.String(150)),
        sa.Column('closure_issuer_designation', sa.String(150)),
        sa.Column('closure_issuer_signature', sa.String(255)),
        sa.Column('closure_receiver_role', sa.String(150)),
        sa.Column('closure_receiver_name', sa.String(150)),
        sa.Column('closure_receiver_signature', sa.String(255)),
        sa.Column('status', sa.String(50)),
        sa.Column('created_by', sa.String(100)),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime()),
    )

    # ===============================
    # composite_work_permit_history
    # ===============================
    op.create_table(
        'composite_work_permit_history',
        sa.Column('history_id', sa.Integer(), primary_key=True),
        sa.Column('cwp_id', sa.Integer()),
        sa.Column('serial_number', sa.String(100)),
        sa.Column('location', sa.String(255)),
        sa.Column('issued_to', sa.String(255)),
        sa.Column('description_of_work', sa.Text()),
        sa.Column('work_from_time', sa.Time()),
        sa.Column('work_from_date', sa.Date()),
        sa.Column('work_to_time', sa.Time()),
        sa.Column('work_to_date', sa.Date()),
        sa.Column('jsa_ref_no', sa.String(100)),
        sa.Column('cross_reference_permits', sa.String(100)),
        sa.Column('isolation_certificate_ref', sa.String(100)),
        sa.Column('electrical_isolation_required', sa.Boolean()),
        sa.Column('electrical_energization_required', sa.Boolean()),
        sa.Column('toolbox_talk_completed', sa.Boolean()),
        sa.Column('status', sa.String(50)),
        sa.Column('created_by', sa.String(100)),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime()),
    )

    # ===============================
    # composite_electrical_isolation_permit
    # ===============================
    op.create_table(
        'composite_electrical_isolation_permit',
        sa.Column('ceip_id', sa.Integer(), primary_key=True),
        sa.Column('composite_work_permit_id', sa.Integer()),
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
        sa.Column('status', sa.String(50)),
        sa.Column('created_by', sa.String(100)),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime()),
    )

    # ===============================
    # composite_electrical_isolation_permit_history
    # ===============================
    op.create_table(
        'composite_electrical_isolation_permit_history',
        sa.Column('history_id', sa.Integer(), primary_key=True),
        sa.Column('ceip_id', sa.Integer()),
        sa.Column('composite_work_permit_id', sa.Integer()),
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
        sa.Column('status', sa.String(50)),
        sa.Column('created_by', sa.String(100)),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime()),
    )

    # ===============================
    # composite_electrical_energization_permit
    # ===============================
    op.create_table(
        'composite_electrical_energization_permit',
        sa.Column('ceep_id', sa.Integer(), primary_key=True),
        sa.Column('composite_work_permit_id', sa.Integer()),
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
        sa.Column('status', sa.String(50)),
        sa.Column('created_by', sa.String(100)),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime()),
    )

    # ===============================
    # composite_electrical_energization_permit_history
    # ===============================
    op.create_table(
        'composite_electrical_energization_permit_history',
        sa.Column('history_id', sa.Integer(), primary_key=True),
        sa.Column('ceep_id', sa.Integer()),
        sa.Column('composite_work_permit_id', sa.Integer()),
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
        sa.Column('status', sa.String(50)),
        sa.Column('created_by', sa.String(100)),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime()),
    )

    # ===============================
    # composite_toolbox_talk
    # ===============================
    op.create_table(
        'composite_toolbox_talk',
        sa.Column('ctt_id', sa.Integer(), primary_key=True),
        sa.Column('composite_work_permit_id', sa.Integer()),
        sa.Column('cross_reference_of_other_permit', sa.String(150)),
        sa.Column('work_clearance_time', sa.Time()),
        sa.Column('work_clearance_date', sa.Date()),
        sa.Column('contractor_engineer_name', sa.String(150)),
        sa.Column('work_installation_unit_facility_name', sa.String(255)),
        sa.Column('tbt_delivered_by', sa.String(150)),
        sa.Column('contract_supervisor_name', sa.String(150)),
        sa.Column('topics_issues_discussed', sa.Text()),
        sa.Column('other_points_raised', sa.Text()),
        sa.Column('status', sa.String(50)),
        sa.Column('created_by', sa.String(100)),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime()),
    )

    # ===============================
    # composite_toolbox_talk_history
    # ===============================
    op.create_table(
        'composite_toolbox_talk_history',
        sa.Column('history_id', sa.Integer(), primary_key=True),
        sa.Column('ctt_id', sa.Integer()),
        sa.Column('composite_work_permit_id', sa.Integer()),
        sa.Column('cross_reference_of_other_permit', sa.String(150)),
        sa.Column('work_clearance_time', sa.Time()),
        sa.Column('work_clearance_date', sa.Date()),
        sa.Column('contractor_engineer_name', sa.String(150)),
        sa.Column('work_installation_unit_facility_name', sa.String(255)),
        sa.Column('tbt_delivered_by', sa.String(150)),
        sa.Column('contract_supervisor_name', sa.String(150)),
        sa.Column('topics_issues_discussed', sa.Text()),
        sa.Column('other_points_raised', sa.Text()),
        sa.Column('status', sa.String(50)),
        sa.Column('created_by', sa.String(100)),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime()),
    )

    # ===============================
    # composite_toolbox_talk_participant
    # ===============================
    op.create_table(
        'composite_toolbox_talk_participant',
        sa.Column('cttp_id', sa.Integer(), primary_key=True),
        sa.Column('toolbox_talk_id', sa.Integer()),
        sa.Column('participant_name', sa.String(150)),
        sa.Column('participant_signature', sa.String(255)),
        sa.Column('created_at', sa.DateTime()),
    )

    # ===============================
    # composite_toolbox_talk_participant_history
    # ===============================
    op.create_table(
        'composite_toolbox_talk_participant_history',
        sa.Column('history_id', sa.Integer(), primary_key=True),
        sa.Column('cttp_id', sa.Integer()),
        sa.Column('toolbox_talk_id', sa.Integer()),
        sa.Column('participant_name', sa.String(150)),
        sa.Column('participant_signature', sa.String(255)),
        sa.Column('created_at', sa.DateTime()),
    )


def downgrade():
    op.drop_table('composite_toolbox_talk_participant_history')
    op.drop_table('composite_toolbox_talk_participant')
    op.drop_table('composite_toolbox_talk_history')
    op.drop_table('composite_toolbox_talk')
    op.drop_table('composite_electrical_energization_permit_history')
    op.drop_table('composite_electrical_energization_permit')
    op.drop_table('composite_electrical_isolation_permit_history')
    op.drop_table('composite_electrical_isolation_permit')
    op.drop_table('composite_work_permit_history')
    op.drop_table('composite_work_permit')