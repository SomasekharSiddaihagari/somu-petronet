"""Recreate composite_work_permit_history table

Revision ID: be9e9ff4313e
Revises: b79218867bdd
Create Date: 2026-01-27 13:10:29.643916

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'be9e9ff4313e'
down_revision: Union[str, Sequence[str], None] = 'b79218867bdd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 🔥 DROP EXISTING TABLE
    op.drop_table("composite_work_permit_history")

    # ✅ CREATE NEW TABLE
    op.create_table(
        "composite_work_permit_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("cwp_id", sa.Integer(), nullable=True),

        # BASIC INFO
        sa.Column("serial_number", sa.String(length=100), nullable=True),
        sa.Column("location", sa.String(length=255), nullable=True),
        sa.Column("issued_to", sa.String(length=255), nullable=True),
        sa.Column("description_of_work", sa.Text(), nullable=True),

        sa.Column("work_from_time", sa.Time(), nullable=True),
        sa.Column("work_from_date", sa.Date(), nullable=True),
        sa.Column("work_to_time", sa.Time(), nullable=True),
        sa.Column("work_to_date", sa.Date(), nullable=True),

        sa.Column("jsa_ref_no", sa.String(length=100), nullable=True),
        sa.Column("cross_reference_permits", sa.String(length=100), nullable=True),
        sa.Column("isolation_certificate_ref", sa.String(length=100), nullable=True),

        # A. GENERAL POINTS
        sa.Column("a1_equipment_area_inspected", sa.String(length=20), nullable=True),
        sa.Column("a2_surrounding_area_checked", sa.String(length=20), nullable=True),
        sa.Column("a3_sewers_manholes_covered", sa.String(length=20), nullable=True),
        sa.Column("a4_hazards_considered", sa.String(length=20), nullable=True),
        sa.Column("a5_equipment_drained", sa.String(length=20), nullable=True),
        sa.Column("a6_equipment_steamed_purged", sa.String(length=20), nullable=True),
        sa.Column("a7_equipment_blinded_isolated", sa.String(length=20), nullable=True),
        sa.Column("a8_equipment_water_flushed", sa.String(length=20), nullable=True),
        sa.Column("a9_iron_sulphide_removed", sa.String(length=20), nullable=True),
        sa.Column("a10_equipment_electrically_isolated", sa.String(length=20), nullable=True),
        sa.Column("a11_gas_test", sa.String(length=20), nullable=True),
        sa.Column("a12_fire_extinguisher_provided", sa.String(length=20), nullable=True),
        sa.Column("a13_area_cordoned", sa.String(length=20), nullable=True),
        sa.Column("a14_ventilation_lighting", sa.String(length=20), nullable=True),

        # B. HOT WORK / CONFINED SPACE
        sa.Column("b1_escape_provided", sa.String(length=20), nullable=True),
        sa.Column("b2_standby_personnel", sa.String(length=20), nullable=True),
        sa.Column("b3_check_oil_gas_trapped", sa.String(length=20), nullable=True),
        sa.Column("b4_shield_against_spark", sa.String(length=20), nullable=True),
        sa.Column("b5_portable_equipment_grounded", sa.String(length=20), nullable=True),
        sa.Column("b6_standby_for_confined_space", sa.String(length=20), nullable=True),

        # C. VEHICLE ENTRY
        sa.Column("c1_peso_spark_elimination", sa.String(length=20), nullable=True),

        # D. EXCAVATION
        sa.Column("d1_excavation_clearance_obtained", sa.String(length=20), nullable=True),

        # REMARKS
        sa.Column("remarks_hazards", sa.Text(), nullable=True),
        sa.Column("additional_requirements_precautions", sa.Text(), nullable=True),

        # ISSUER / RECEIVER
        sa.Column("issuer_name", sa.String(length=150), nullable=True),
        sa.Column("issuer_designation", sa.String(length=150), nullable=True),
        sa.Column("issuer_signature", sa.String(length=255), nullable=True),

        sa.Column("receiver_role", sa.String(length=150), nullable=True),
        sa.Column("receiver_name", sa.String(length=150), nullable=True),
        sa.Column("receiver_signature", sa.String(length=255), nullable=True),

        # ELECTRICAL
        sa.Column("electrical_isolation_required", sa.Boolean(), nullable=True),
        sa.Column("electrical_energization_required", sa.Boolean(), nullable=True),

        # TOOLBOX
        sa.Column("toolbox_talk_completed", sa.Boolean(), nullable=True),

        # GAS TEST
        sa.Column("gas_test_from_time", sa.Time(), nullable=True),
        sa.Column("gas_test_to_time", sa.Time(), nullable=True),
        sa.Column("gas_test_from_date", sa.Date(), nullable=True),
        sa.Column("gas_test_to_date", sa.Date(), nullable=True),

        sa.Column("gas_hcs_percent", sa.String(length=50), nullable=True),
        sa.Column("gas_toxic_ppm", sa.String(length=50), nullable=True),
        sa.Column("gas_o2_percent", sa.String(length=50), nullable=True),

        sa.Column("gas_additional_precautions", sa.Text(), nullable=True),

        sa.Column("gas_issuer_name", sa.String(length=150), nullable=True),
        sa.Column("gas_issuer_designation", sa.String(length=150), nullable=True),
        sa.Column("gas_issuer_signature", sa.String(length=255), nullable=True),

        sa.Column("gas_receiver_name", sa.String(length=150), nullable=True),
        sa.Column("gas_receiver_designation", sa.String(length=150), nullable=True),
        sa.Column("gas_receiver_signature", sa.String(length=255), nullable=True),

        # CLOSURE
        sa.Column("closure_issuer_name", sa.String(length=150), nullable=True),
        sa.Column("closure_issuer_designation", sa.String(length=150), nullable=True),
        sa.Column("closure_issuer_signature", sa.String(length=255), nullable=True),

        sa.Column("closure_receiver_role", sa.String(length=150), nullable=True),
        sa.Column("closure_receiver_name", sa.String(length=150), nullable=True),
        sa.Column("closure_receiver_signature", sa.String(length=255), nullable=True),

        # SYSTEM
        sa.Column("status", sa.String(length=50), nullable=True),
        sa.Column("created_by", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=True),
    )


def downgrade():
    op.drop_table("composite_work_permit_history")