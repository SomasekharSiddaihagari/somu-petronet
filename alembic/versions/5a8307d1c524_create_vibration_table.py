"""create vibration table

Revision ID: 5a8307d1c524
Revises: 308021acee4e
Create Date: 2026-01-22 20:02:41.391504

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a8307d1c524'
down_revision: Union[str, Sequence[str], None] = '308021acee4e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # =====================================================
    # vibration_temperature_master_ner
    # =====================================================
    op.create_table(
        "vibration_temperature_master_ner",
        sa.Column("vtmn_id", sa.Integer(), primary_key=True, autoincrement=True),

        sa.Column("station", sa.String(100)),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("shift", sa.String(50)),
        sa.Column("start_time", sa.Time()),
        sa.Column("logbook_date", sa.Date()),

        sa.Column("shift_engineer_a_name", sa.String(100)),
        sa.Column("shift_engineer_a_signature", sa.String(255)),

        sa.Column("technician_c_name", sa.String(100)),
        sa.Column("technician_c_signature", sa.String(255)),

        sa.Column("shift_engineer_b_name", sa.String(100)),
        sa.Column("shift_engineer_b_signature", sa.String(255)),

        sa.Column("created_by", sa.String(100)),
        sa.Column("created_at", sa.DateTime()),
        sa.Column("updated_at", sa.DateTime()),
    )

    # =====================================================
    # vibration_temperature_master_ner_history
    # =====================================================
    op.create_table(
        "vibration_temperature_master_ner_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("vtmn_id", sa.Integer()),

        sa.Column("station", sa.String(100)),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("shift", sa.String(50)),
        sa.Column("start_time", sa.Time()),
        sa.Column("logbook_date", sa.Date()),

        sa.Column("shift_engineer_a_name", sa.String(100)),
        sa.Column("shift_engineer_a_signature", sa.String(255)),

        sa.Column("technician_c_name", sa.String(100)),
        sa.Column("technician_c_signature", sa.String(255)),

        sa.Column("shift_engineer_b_name", sa.String(100)),
        sa.Column("shift_engineer_b_signature", sa.String(255)),

        sa.Column("created_by", sa.String(100)),
        sa.Column("created_at", sa.DateTime()),
        sa.Column("updated_at", sa.DateTime()),
    )

    # =====================================================
    # vibration_temperature_master_mlr
    # =====================================================
    op.create_table(
        "vibration_temperature_master_mlr",
        sa.Column("vtm_id", sa.Integer(), primary_key=True, autoincrement=True),

        sa.Column("station", sa.String(100)),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("shift", sa.String(50)),
        sa.Column("start_time", sa.Time()),
        sa.Column("logbook_date", sa.Date()),

        sa.Column("shift_engineer_a_name", sa.String(100)),
        sa.Column("shift_engineer_a_signature", sa.String(255)),

        sa.Column("technician_c_name", sa.String(100)),
        sa.Column("technician_c_signature", sa.String(255)),

        sa.Column("shift_engineer_b_name", sa.String(100)),
        sa.Column("shift_engineer_b_signature", sa.String(255)),

        sa.Column("created_by", sa.String(100)),
        sa.Column("created_at", sa.DateTime()),
        sa.Column("updated_at", sa.DateTime()),
    )

    # =====================================================
    # vibration_temperature_master_mlr_history
    # =====================================================
    op.create_table(
        "vibration_temperature_master_mlr_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("vtm_id", sa.Integer()),

        sa.Column("station", sa.String(100)),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("shift", sa.String(50)),
        sa.Column("start_time", sa.Time()),
        sa.Column("logbook_date", sa.Date()),

        sa.Column("shift_engineer_a_name", sa.String(100)),
        sa.Column("shift_engineer_a_signature", sa.String(255)),

        sa.Column("technician_c_name", sa.String(100)),
        sa.Column("technician_c_signature", sa.String(255)),

        sa.Column("shift_engineer_b_name", sa.String(100)),
        sa.Column("shift_engineer_b_signature", sa.String(255)),

        sa.Column("created_by", sa.String(100)),
        sa.Column("created_at", sa.DateTime()),
        sa.Column("updated_at", sa.DateTime()),
    )

    # =====================================================
    # vibration_temperature_entry (MLR)
    # =====================================================
    op.create_table(
        "vibration_temperature_entry",
        sa.Column("vte_id", sa.Integer(), primary_key=True, autoincrement=True),

        sa.Column(
            "master_id",
            sa.Integer(),
            sa.ForeignKey("vibration_temperature_master_mlr.vtm_id"),
        ),

        sa.Column("entry_date", sa.Date()),
        sa.Column("entry_time", sa.Time()),
        sa.Column("mlp101_a_b_c", sa.String(50)),

        sa.Column("pump_vib_de_x", sa.Float()),
        sa.Column("pump_vib_de_y", sa.Float()),
        sa.Column("pump_vib_nde_x", sa.Float()),
        sa.Column("pump_vib_nde_y", sa.Float()),

        sa.Column("pump_thrust_x", sa.Float()),
        sa.Column("pump_thrust_y", sa.Float()),

        sa.Column("motor_bearing_vib_de_x", sa.Float()),
        sa.Column("motor_bearing_vib_de_y", sa.Float()),
        sa.Column("motor_bearing_vib_nde_x", sa.Float()),
        sa.Column("motor_bearing_vib_nde_y", sa.Float()),

        sa.Column("motor_winding_ch1", sa.Float()),
        sa.Column("motor_winding_ch2", sa.Float()),
        sa.Column("motor_winding_ch3", sa.Float()),

        sa.Column("motor_winding_ch4", sa.Float()),
        sa.Column("motor_winding_ch5", sa.Float()),
        sa.Column("motor_winding_ch6", sa.Float()),

        sa.Column("motor_bearing_temp_de", sa.Float()),
        sa.Column("motor_bearing_temp_nde", sa.Float()),

        sa.Column("pump_body_temperature", sa.Float()),

        sa.Column("pump_bearing_temp_de_x", sa.Float()),
        sa.Column("pump_bearing_temp_de_y", sa.Float()),
        sa.Column("pump_bearing_temp_nde_x", sa.Float()),
        sa.Column("pump_bearing_temp_nde_y", sa.Float()),
        sa.Column("pump_bearing_thrust_x", sa.Float()),
        sa.Column("pump_bearing_thrust_y", sa.Float()),

        sa.Column("created_by", sa.String(100)),
        sa.Column("created_at", sa.DateTime()),
    )

    # =====================================================
    # vibration_temperature_entry_history (MLR)
    # =====================================================
    op.create_table(
        "vibration_temperature_entry_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("vte_id", sa.Integer()),
        sa.Column("master_id", sa.Integer()),

        sa.Column("entry_date", sa.Date()),
        sa.Column("entry_time", sa.Time()),
        sa.Column("mlp101_a_b_c", sa.String(50)),

        sa.Column("pump_vib_de_x", sa.Float()),
        sa.Column("pump_vib_de_y", sa.Float()),
        sa.Column("pump_vib_nde_x", sa.Float()),
        sa.Column("pump_vib_nde_y", sa.Float()),

        sa.Column("pump_thrust_x", sa.Float()),
        sa.Column("pump_thrust_y", sa.Float()),

        sa.Column("motor_bearing_vib_de_x", sa.Float()),
        sa.Column("motor_bearing_vib_de_y", sa.Float()),
        sa.Column("motor_bearing_vib_nde_x", sa.Float()),
        sa.Column("motor_bearing_vib_nde_y", sa.Float()),

        sa.Column("motor_winding_ch1", sa.Float()),
        sa.Column("motor_winding_ch2", sa.Float()),
        sa.Column("motor_winding_ch3", sa.Float()),

        sa.Column("motor_winding_ch4", sa.Float()),
        sa.Column("motor_winding_ch5", sa.Float()),
        sa.Column("motor_winding_ch6", sa.Float()),

        sa.Column("motor_bearing_temp_de", sa.Float()),
        sa.Column("motor_bearing_temp_nde", sa.Float()),

        sa.Column("pump_body_temperature", sa.Float()),

        sa.Column("pump_bearing_temp_de_x", sa.Float()),
        sa.Column("pump_bearing_temp_de_y", sa.Float()),
        sa.Column("pump_bearing_temp_nde_x", sa.Float()),
        sa.Column("pump_bearing_temp_nde_y", sa.Float()),
        sa.Column("pump_bearing_thrust_x", sa.Float()),
        sa.Column("pump_bearing_thrust_y", sa.Float()),

        sa.Column("created_by", sa.String(100)),
        sa.Column("created_at", sa.DateTime()),
    )

    # =====================================================
    # vibration_temperature_entry_ner
    # =====================================================
    op.create_table(
        "vibration_temperature_entry_ner",
        sa.Column("vten_id", sa.Integer(), primary_key=True, autoincrement=True),

        sa.Column("master_id", sa.Integer()),

        sa.Column("entry_date", sa.Date()),
        sa.Column("entry_time", sa.Time()),
        sa.Column("mlp101_a_b_c", sa.String(50)),

        sa.Column("pump_vib_de_x", sa.Float()),
        sa.Column("pump_vib_de_y", sa.Float()),
        sa.Column("pump_vib_nde_x", sa.Float()),
        sa.Column("pump_vib_nde_y", sa.Float()),

        sa.Column("pump_thrust_x", sa.Float()),
        sa.Column("pump_thrust_y", sa.Float()),

        sa.Column("motor_bearing_vib_de_x", sa.Float()),
        sa.Column("motor_bearing_vib_de_y", sa.Float()),
        sa.Column("motor_bearing_vib_nde_x", sa.Float()),
        sa.Column("motor_bearing_vib_nde_y", sa.Float()),

        sa.Column("motor_winding_ch1", sa.Float()),
        sa.Column("motor_winding_ch2", sa.Float()),
        sa.Column("motor_winding_ch3", sa.Float()),

        sa.Column("motor_winding_ch4", sa.Float()),
        sa.Column("motor_winding_ch5", sa.Float()),
        sa.Column("motor_winding_ch6", sa.Float()),

        sa.Column("motor_bearing_temp_de", sa.Float()),
        sa.Column("motor_bearing_temp_nde", sa.Float()),

        sa.Column("pump_body_temperature", sa.Float()),

        sa.Column("pump_bearing_temp_de_x", sa.Float()),
        sa.Column("pump_bearing_temp_de_y", sa.Float()),
        sa.Column("pump_bearing_temp_nde_x", sa.Float()),
        sa.Column("pump_bearing_temp_nde_y", sa.Float()),
        sa.Column("pump_bearing_thrust_x", sa.Float()),
        sa.Column("pump_bearing_thrust_y", sa.Float()),

        sa.Column("created_by", sa.String(100)),
        sa.Column("created_at", sa.DateTime()),
    )

    # =====================================================
    # vibration_temperature_entry_ner_history
    # =====================================================
    op.create_table(
        "vibration_temperature_entry_ner_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("vten_id", sa.Integer()),
        sa.Column("master_id", sa.Integer()),

        sa.Column("entry_date", sa.Date()),
        sa.Column("entry_time", sa.Time()),
        sa.Column("mlp101_a_b_c", sa.String(50)),

        sa.Column("pump_vib_de_x", sa.Float()),
        sa.Column("pump_vib_de_y", sa.Float()),
        sa.Column("pump_vib_nde_x", sa.Float()),
        sa.Column("pump_vib_nde_y", sa.Float()),

        sa.Column("pump_thrust_x", sa.Float()),
        sa.Column("pump_thrust_y", sa.Float()),

        sa.Column("motor_bearing_vib_de_x", sa.Float()),
        sa.Column("motor_bearing_vib_de_y", sa.Float()),
        sa.Column("motor_bearing_vib_nde_x", sa.Float()),
        sa.Column("motor_bearing_vib_nde_y", sa.Float()),

        sa.Column("motor_winding_ch1", sa.Float()),
        sa.Column("motor_winding_ch2", sa.Float()),
        sa.Column("motor_winding_ch3", sa.Float()),

        sa.Column("motor_winding_ch4", sa.Float()),
        sa.Column("motor_winding_ch5", sa.Float()),
        sa.Column("motor_winding_ch6", sa.Float()),

        sa.Column("motor_bearing_temp_de", sa.Float()),
        sa.Column("motor_bearing_temp_nde", sa.Float()),

        sa.Column("pump_body_temperature", sa.Float()),

        sa.Column("pump_bearing_temp_de_x", sa.Float()),
        sa.Column("pump_bearing_temp_de_y", sa.Float()),
        sa.Column("pump_bearing_temp_nde_x", sa.Float()),
        sa.Column("pump_bearing_temp_nde_y", sa.Float()),
        sa.Column("pump_bearing_thrust_x", sa.Float()),
        sa.Column("pump_bearing_thrust_y", sa.Float()),

        sa.Column("created_by", sa.String(100)),
        sa.Column("created_at", sa.DateTime()),
    )


def downgrade():
    op.drop_table("vibration_temperature_entry_ner_history")
    op.drop_table("vibration_temperature_entry_ner")
    op.drop_table("vibration_temperature_entry_history")
    op.drop_table("vibration_temperature_entry")
    op.drop_table("vibration_temperature_master_mlr_history")
    op.drop_table("vibration_temperature_master_mlr")
    op.drop_table("vibration_temperature_master_ner_history")
    op.drop_table("vibration_temperature_master_ner")