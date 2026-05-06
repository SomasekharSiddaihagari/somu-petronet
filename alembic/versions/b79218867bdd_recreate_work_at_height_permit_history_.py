"""Recreate work_at_height_permit_history table

Revision ID: b79218867bdd
Revises: 901e10a54cd4
Create Date: 2026-01-27 12:57:10.931529

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b79218867bdd'
down_revision: Union[str, Sequence[str], None] = '901e10a54cd4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 🔥 DROP EXISTING TABLE
    op.drop_table("work_at_height_permit_history")

    # ✅ CREATE NEW TABLE
    op.create_table(
        "work_at_height_permit_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("whp_id", sa.Integer(), nullable=True),

        sa.Column("serial_number", sa.String(length=150), nullable=True),
        sa.Column("section_contractor_name", sa.String(length=255), nullable=True),
        sa.Column("nature_of_work", sa.Text(), nullable=True),

        sa.Column("work_from_time", sa.Time(), nullable=True),
        sa.Column("work_from_date", sa.Date(), nullable=True),
        sa.Column("work_to_time", sa.Time(), nullable=True),
        sa.Column("work_to_date", sa.Date(), nullable=True),

        sa.Column("location", sa.String(length=255), nullable=True),

        # SAFETY CHECKLIST
        sa.Column("sc1_equipment_work_area_inspected", sa.String(length=20), nullable=True),
        sa.Column("sc2_surrounding_area_checked", sa.String(length=20), nullable=True),
        sa.Column("sc3_sewers_manholes_covered", sa.String(length=20), nullable=True),
        sa.Column("sc4_scaffolds_ladders_checked", sa.String(length=20), nullable=True),
        sa.Column("sc5_materials_fall_protected", sa.String(length=20), nullable=True),
        sa.Column("sc6_isi_marked_belts_helmets", sa.String(length=20), nullable=True),
        sa.Column("sc7_contractor_fit_for_height", sa.String(length=20), nullable=True),
        sa.Column("sc8_instructions_given", sa.String(length=20), nullable=True),
        sa.Column("sc9_proper_illumination", sa.String(length=20), nullable=True),
        sa.Column("sc10_adequate_platform_space", sa.String(length=20), nullable=True),
        sa.Column("sc11_proper_exit_means", sa.String(length=20), nullable=True),
        sa.Column("sc12_precautionary_tags_boards", sa.String(length=20), nullable=True),
        sa.Column("sc13_portable_equipment_earthed", sa.String(length=20), nullable=True),
        sa.Column("sc14_elcb_switches_provided", sa.String(length=20), nullable=True),
        sa.Column("sc15_standby_supervision_provided", sa.String(length=20), nullable=True),
        sa.Column("sc16_workers_trained_safety_belts", sa.String(length=20), nullable=True),
        sa.Column("sc17_operations_incharge_informed", sa.String(length=20), nullable=True),
        sa.Column("sc18_area_cordoned_off", sa.String(length=20), nullable=True),
        sa.Column("sc19_precautions_against_public_traffic", sa.String(length=20), nullable=True),
        sa.Column("sc20_fire_extinguisher_provided", sa.String(length=20), nullable=True),

        # INSTRUCTIONS & REMARKS
        sa.Column("special_instructions", sa.Text(), nullable=True),
        sa.Column("additional_remarks", sa.Text(), nullable=True),

        # ISSUER / RECEIVER
        sa.Column("issuer_designation", sa.String(length=150), nullable=True),
        sa.Column("issuer_name", sa.String(length=150), nullable=True),
        sa.Column("issuer_signature", sa.String(length=255), nullable=True),

        sa.Column("receiver_role", sa.String(length=150), nullable=True),
        sa.Column("receiver_name", sa.String(length=150), nullable=True),
        sa.Column("receiver_signature", sa.String(length=255), nullable=True),

        # FLAGS
        sa.Column("electrical_isolation_required", sa.Boolean(), nullable=True),
        sa.Column("electrical_energization_required", sa.Boolean(), nullable=True),
        sa.Column("toolbox_talk_required", sa.Boolean(), nullable=True),

        # RENEWAL
        sa.Column("renewal_from_date", sa.Date(), nullable=True),
        sa.Column("renewal_from_time", sa.Time(), nullable=True),
        sa.Column("renewal_to_date", sa.Date(), nullable=True),
        sa.Column("renewal_to_time", sa.Time(), nullable=True),

        sa.Column("renewal_issuer_name", sa.String(length=150), nullable=True),
        sa.Column("renewal_issuer_designation", sa.String(length=150), nullable=True),
        sa.Column("renewal_issuer_signature", sa.String(length=255), nullable=True),

        sa.Column("renewal_receiver_name", sa.String(length=150), nullable=True),
        sa.Column("renewal_receiver_designation", sa.String(length=150), nullable=True),
        sa.Column("renewal_receiver_signature", sa.String(length=255), nullable=True),

        sa.Column("renewal_toolbox_talk", sa.Boolean(), nullable=True),

        # CLOSURE
        sa.Column("closure_issuer_designation", sa.String(length=150), nullable=True),
        sa.Column("closure_issuer_name", sa.String(length=150), nullable=True),
        sa.Column("closure_issuer_signature", sa.String(length=255), nullable=True),

        sa.Column("closure_receiver_role", sa.String(length=150), nullable=True),
        sa.Column("closure_receiver_name", sa.String(length=150), nullable=True),
        sa.Column("closure_receiver_signature", sa.String(length=255), nullable=True),

        # JOB COMPLETION
        sa.Column("job_completion_time", sa.Time(), nullable=True),
        sa.Column("job_completion_date", sa.Date(), nullable=True),
        sa.Column("work_status", sa.Text(), nullable=True),

        # SYSTEM
        sa.Column("status", sa.String(length=50), nullable=True),
        sa.Column("created_by", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=True),
    )


def downgrade():
    # Rollback = just drop the table
    op.drop_table("work_at_height_permit_history")