"""create fire tables

Revision ID: 5e38bb16aa83
Revises: acbce9150fc0
Create Date: 2026-01-21 15:41:53.224158

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e38bb16aa83'
down_revision: Union[str, Sequence[str], None] = 'acbce9150fc0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # =====================================================
    # FIRE ENGINE TEST MASTER
    # =====================================================
    op.create_table(
        "fire_engine_test_master",
        sa.Column("fire_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("document_number", sa.String(100)),
        sa.Column("station_name", sa.String(100)),
        sa.Column("station_incharge", sa.String(100)),
        sa.Column("shift", sa.String(20)),
        sa.Column("start_time", sa.Time),
        sa.Column("log_date", sa.Date),
        sa.Column("technician_name", sa.String(100)),
        sa.Column("technician_signature", sa.Text),
        sa.Column("engineer_name", sa.String(100)),
        sa.Column("engineer_signature", sa.Text),
        sa.Column("status", sa.String(50)),
        sa.Column("created_by", sa.Integer),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # =====================================================
    # FIRE ENGINE TEST ENTRY
    # =====================================================
    op.create_table(
        "fire_engine_test_entry",
        sa.Column("fire_entry_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column(
            "master_id",
            sa.Integer,
            sa.ForeignKey("fire_engine_test_master.fire_id", ondelete="CASCADE"),
        ),
        sa.Column("entry_date", sa.Date),
        sa.Column("fire_engine_no", sa.String(50)),
        sa.Column("time_start", sa.Time),
        sa.Column("time_stop", sa.Time),
        sa.Column("running_hours", sa.Float),
        sa.Column("battery_voltage", sa.String(20)),
        sa.Column("lube_oil_level", sa.String(20)),
        sa.Column("fuel_level_lts", sa.Float),
        sa.Column("radiator_water_level", sa.String(20)),
        sa.Column("lube_oil_temp", sa.Float),
        sa.Column("lube_oil_pressure", sa.Float),
        sa.Column("fwt_1", sa.Float),
        sa.Column("fwt_2", sa.Float),
        sa.Column("fwt_3", sa.Float),
        sa.Column("cooling_water_temp", sa.Float),
        sa.Column("rpm", sa.Integer),
        sa.Column("mode_of_test", sa.String(50)),
        sa.Column("tech_sign", sa.String(100)),
        sa.Column("engg_sign", sa.String(100)),
        sa.Column("remarks", sa.Text),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # =====================================================
    # FIRE ENGINE TEST MASTER HISTORY
    # =====================================================
    op.create_table(
        "fire_engine_test_master_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("document_number", sa.String(100)),
        sa.Column("fire_id", sa.Integer),
        sa.Column("station_name", sa.String(100)),
        sa.Column("station_incharge", sa.String(100)),
        sa.Column("shift", sa.String(20)),
        sa.Column("start_time", sa.Time),
        sa.Column("log_date", sa.Date),
        sa.Column("technician_name", sa.String(100)),
        sa.Column("technician_signature", sa.Text),
        sa.Column("engineer_name", sa.String(100)),
        sa.Column("engineer_signature", sa.Text),
        sa.Column("status", sa.String(50)),
        sa.Column("created_by", sa.Integer),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now()),
    )

    # =====================================================
    # FIRE ENGINE TEST ENTRY HISTORY
    # =====================================================
    op.create_table(
        "fire_engine_test_entry_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("master_id", sa.Integer),
        sa.Column("fire_entry_id", sa.Integer),
        sa.Column("entry_date", sa.Date),
        sa.Column("fire_engine_no", sa.String(50)),
        sa.Column("time_start", sa.Time),
        sa.Column("time_stop", sa.Time),
        sa.Column("running_hours", sa.Float),
        sa.Column("battery_voltage", sa.String(20)),
        sa.Column("lube_oil_level", sa.String(20)),
        sa.Column("fuel_level_lts", sa.Float),
        sa.Column("radiator_water_level", sa.String(20)),
        sa.Column("lube_oil_temp", sa.Float),
        sa.Column("lube_oil_pressure", sa.Float),
        sa.Column("fwt_1", sa.Float),
        sa.Column("fwt_2", sa.Float),
        sa.Column("fwt_3", sa.Float),
        sa.Column("cooling_water_temp", sa.Float),
        sa.Column("rpm", sa.Integer),
        sa.Column("mode_of_test", sa.String(50)),
        sa.Column("tech_sign", sa.String(100)),
        sa.Column("engg_sign", sa.String(100)),
        sa.Column("remarks", sa.Text),
        sa.Column("action", sa.String(50)),
        sa.Column("action_by", sa.Integer),
        sa.Column("action_at", sa.DateTime, server_default=sa.func.now()),
    )

    # =====================================================
    # NER DIGITAL LOGBOOK
    # =====================================================
    op.create_table(
        "ner_digital_logbook",
        sa.Column("ner_logbook_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("logbook_ref_no", sa.String(50)),
        sa.Column("station", sa.String(100)),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("shift", sa.String(20)),
        sa.Column("log_date", sa.Date),
        sa.Column("start_time", sa.Time),
        sa.Column("handed_over_by", sa.String(100)),
        sa.Column("taken_over_by", sa.String(100)),
        sa.Column("is_shift_closed", sa.Boolean),
        sa.Column("created_by", sa.Integer),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # =====================================================
    # NER DIGITAL LOGBOOK ENTRY
    # =====================================================
    op.create_table(
        "ner_digital_logbook_entry",
        sa.Column("ner_entry_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column(
            "ner_logbook_id",
            sa.Integer,
            sa.ForeignKey("ner_digital_logbook.ner_logbook_id", ondelete="CASCADE"),
        ),
        sa.Column("entry_time", sa.Time),
        sa.Column("location", sa.String(100)),
        sa.Column("dkn", sa.String(50)),
        sa.Column("hsn", sa.String(50)),
        sa.Column("mlr", sa.String(50)),
        sa.Column("sv3", sa.String(50)),
        sa.Column("sv4", sa.String(50)),
        sa.Column("created_by", sa.Integer),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # =====================================================
    # NER DIGITAL LOGBOOK HISTORY
    # =====================================================
    op.create_table(
        "ner_digital_logbook_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("ner_logbook_id", sa.Integer),
        sa.Column("logbook_ref_no", sa.String(50)),
        sa.Column("station", sa.String(100)),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("shift", sa.String(20)),
        sa.Column("log_date", sa.Date),
        sa.Column("start_time", sa.Time),
        sa.Column("handed_over_by", sa.String(100)),
        sa.Column("taken_over_by", sa.String(100)),
        sa.Column("is_shift_closed", sa.Boolean),
        sa.Column("created_by", sa.Integer),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now()),
    )

    # =====================================================
    # NER DIGITAL LOGBOOK ENTRY HISTORY
    # =====================================================
    op.create_table(
        "ner_digital_logbook_entry_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("ner_entry_id", sa.Integer),
        sa.Column("ner_logbook_id", sa.Integer),
        sa.Column("entry_time", sa.Time),
        sa.Column("location", sa.String(100)),
        sa.Column("dkn", sa.String(50)),
        sa.Column("hsn", sa.String(50)),
        sa.Column("mlr", sa.String(50)),
        sa.Column("sv3", sa.String(50)),
        sa.Column("sv4", sa.String(50)),
        sa.Column("created_by", sa.Integer),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table("ner_digital_logbook_entry_history")
    op.drop_table("ner_digital_logbook_history")
    op.drop_table("ner_digital_logbook_entry")
    op.drop_table("ner_digital_logbook")

    op.drop_table("fire_engine_test_entry_history")
    op.drop_table("fire_engine_test_master_history")
    op.drop_table("fire_engine_test_entry")
    op.drop_table("fire_engine_test_master")