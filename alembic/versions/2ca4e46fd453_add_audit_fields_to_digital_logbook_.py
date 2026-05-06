"""add audit fields to digital logbook tables

Revision ID: 2ca4e46fd453
Revises: 4caeaa34d57a
Create Date: 2026-01-28 18:00:25.348253

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ca4e46fd453'
down_revision: Union[str, Sequence[str], None] = '4caeaa34d57a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


TABLES = [
    "a_shift_log",
    "a_shift_log_history",
    "access_control_station",
    "access_control_station_history",
    "b_shift_log",
    "b_shift_log_history",
    "cp_reading_dkn_entry",
    "cp_reading_dkn_entry_history",
    "cp_reading_dkn_master",
    "cp_reading_dkn_master_history",
    "cp_reading_hsn_entry",
    "cp_reading_hsn_entry_history",
    "cp_reading_hsn_master",
    "cp_reading_hsn_master_history",
    "cp_reading_mlr_entry",
    "cp_reading_mlr_entry_history",
    "cp_reading_mlr_master",
    "cp_reading_mlr_master_history",
    "cp_reading_ner_entry",
    "cp_reading_ner_entry_history",
    "cp_reading_ner_master",
    "daily_safety_checklist",
    "daily_safety_checklist_history",
    "daily_sampling_entry",
    "daily_sampling_entry_history",
    "daily_sampling_master",
    "daily_sampling_master_history",
    "dg_250kva_entry",
    "dg_250kva_entry_history",
    "dg_250kva_master",
    "dg_250kva_master_history",
    "dkn_digital_logbook",
    "dkn_digital_logbook_entry",
    "dkn_digital_logbook_entry_history",
    "dkn_digital_logbook_history",
    "erv_c_shift_log",
    "erv_c_shift_log_history",
    "erv_logbook_master",
    "erv_logbook_master_history",
    "erv_vehicle_inspection_log",
    "erv_vehicle_inspection_log_history",
    "fire_engine_test_entry",
    "fire_engine_test_entry_history",
    "fire_engine_test_master",
    "fire_engine_test_master_history",
    "hsn_digital_logbook",
    "hsn_digital_logbook_entry",
    "hsn_digital_logbook_entry_history",
    "hsn_digital_logbook_history",
    "kptcl_dkn_entry",
    "kptcl_dkn_entry_history",
    "kptcl_dkn_master",
    "kptcl_dkn_master_history",
    "kptcl_hsn_entry",
    "kptcl_hsn_entry_history",
    "kptcl_hsn_master",
    "kptcl_hsn_master_history",
    "kptcl_ner_entry",
    "kptcl_ner_entry_history",
    "kptcl_ner_master",
    "kptcl_ner_master_history",
    "line_walker_entry",
    "line_walker_entry_history",
    "line_walker_master",
    "line_walker_master_history",
    "location_access_approval",
    "location_access_approval_history",
    "location_access_token",
    "location_access_token_history",
    "logbook_shift_master",
    "logbook_shift_master_history",
    "mfm_accounting_dkn",
    "mfm_accounting_dkn_history",
    "mfm_accounting_hsn",
    "mfm_accounting_hsn_history",
    "mfm_log_entry_dkn",
    "mfm_log_entry_dkn_history",
    "mfm_log_hsn2_entry",
    "mfm_log_hsn2_entry_history",
    "mfm_log_hsn2_master",
    "mfm_log_hsn2_master_history",
    "mfm_log_hsn_entry",
    "mfm_log_hsn_entry_history",
    "mfm_log_hsn_master",
    "mfm_log_hsn_master_history",
    "mfm_log_master_dkn",
    "mfm_log_master_dkn_history",
    "mfm_log_mlr_entry",
    "mfm_log_mlr_entry_history",
    "mfm_log_mlr_entry_two_history",
    "mfm_log_mlr_master",
    "mfm_log_mlr_master_history",
    "mfm_log_mlr_master_two",
    "mfm_log_mlr_master_two_history",
    "mfm_log_mlr_two_entry",
    "mfm_log_ner_entry",
    "mfm_log_ner_entry_history",
    "mfm_log_ner_master",
    "mfm_log_ner_master_history",
    "mfm_log_ner_page2_master",
    "mfm_plt_detail_dkn",
    "mfm_plt_detail_dkn_history",
    "mfm_shutdown_detail_dkn",
    "mfm_shutdown_detail_dkn_history",
    "mlr_digital_logbook",
    "mlr_digital_logbook_entry",
    "mlr_digital_logbook_entry_history",
    "mlr_digital_logbook_history",
    "ner_digital_logbook",
    "ner_digital_logbook_entry",
    "ner_digital_logbook_entry_history",
    "ner_digital_logbook_history",
    "npt_report_entry",
    "npt_report_entry_history",
    "npt_report_master",
    "npt_report_master_history",
    "pressure_log_master",
    "pressure_log_master_history",
    "product_dispatch_hourly_log",
    "product_dispatch_hourly_log_history",
    "product_dispatch_shutdown_log",
    "product_dispatch_shutdown_log_history",
    "security_guard_report",
    "security_guard_report_history",
    "shift",
    "shift_handover_log",
    "shift_handover_log_history",
    "shift_handover_master",
    "shift_handover_master_history",
    "shift_handover_task",
    "shift_handover_task_history",
    "shift_history",
    "shift_takeover",
    "shift_takeover_history",
    "station_shift_incharge",
    "station_shift_incharge_history",
    "supervisor_entry",
    "supervisor_entry_history",
    "tank_10kl_ffe_entry",
    "tank_10kl_ffe_entry_history",
    "tank_10kl_ffe_master",
    "tank_10kl_ffe_master_history",
    "tank_dip_memo",
    "tank_dip_memo_history",
    "vibration_temperature_entry",
    "vibration_temperature_entry_history",
    "vibration_temperature_entry_ner",
    "vibration_temperature_entry_ner_history",
    "vibration_temperature_master_mlr",
    "vibration_temperature_master_mlr_history",
    "vibration_temperature_master_ner",
    "vibration_temperature_master_ner_history",
]

def upgrade():
    for table in TABLES:
        op.execute(f"""
        DO $$
        BEGIN
            IF to_regclass('public.{table}') IS NOT NULL THEN
                ALTER TABLE "{table}" ADD COLUMN IF NOT EXISTS created_by BIGINT;
                ALTER TABLE "{table}" ADD COLUMN IF NOT EXISTS created_at TIMESTAMP;
                ALTER TABLE "{table}" ADD COLUMN IF NOT EXISTS updated_by BIGINT;
                ALTER TABLE "{table}" ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP;
            END IF;
        END $$;
        """)


def downgrade():
    pass