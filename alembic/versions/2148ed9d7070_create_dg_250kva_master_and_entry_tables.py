"""create dg 250kva master and entry tables

Revision ID: 2148ed9d7070
Revises: a318ca1b4ff4
Create Date: 2026-01-21 18:32:16.164540

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2148ed9d7070'
down_revision: Union[str, Sequence[str], None] = 'a318ca1b4ff4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():

    # -----------------------------------
    # dg_250kva_master
    # -----------------------------------
    op.create_table(
        "dg_250kva_master",
        sa.Column("dg_id", sa.Integer, primary_key=True, autoincrement=True),

        sa.Column("station", sa.String(50)),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("shift", sa.String(10)),
        sa.Column("start_time", sa.Time),
        sa.Column("entry_date", sa.Date),
        sa.Column("status", sa.String(20)),
        sa.Column("document_number", sa.String(100)),

        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # -----------------------------------
    # dg_250kva_master_history
    # -----------------------------------
    op.create_table(
        "dg_250kva_master_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("dg_id", sa.Integer),

        sa.Column("station", sa.String(50)),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("shift", sa.String(10)),
        sa.Column("start_time", sa.Time),
        sa.Column("entry_date", sa.Date),
        sa.Column("status", sa.String(20)),
        sa.Column("document_number", sa.String(100)),

        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # -----------------------------------
    # dg_250kva_entry
    # -----------------------------------
    op.create_table(
        "dg_250kva_entry",
        sa.Column("dg_entry_id", sa.Integer, primary_key=True, autoincrement=True),

        sa.Column(
            "master_id",
            sa.Integer,
            sa.ForeignKey(
                "dg_250kva_master.dg_id",
                ondelete="CASCADE"
            ),
        ),

        sa.Column("log_date", sa.Date),

        sa.Column("start_time", sa.Time),
        sa.Column("stop_time", sa.Time),
        sa.Column("run_time", sa.String(20)),

        sa.Column("cumulative", sa.Float),
        sa.Column("hmr", sa.Float),
        sa.Column("battery_voltage", sa.Float),
        sa.Column("lube_oil_pressure", sa.Float),
        sa.Column("rpm", sa.Float),
        sa.Column("electrical_hmr", sa.Float),
        sa.Column("water_temperature", sa.Float),

        sa.Column("voltage_load", sa.Float),
        sa.Column("voltage_ry", sa.Float),
        sa.Column("voltage_yb", sa.Float),
        sa.Column("voltage_br", sa.Float),

        sa.Column("current_r", sa.Float),
        sa.Column("current_y", sa.Float),
        sa.Column("current_b", sa.Float),

        sa.Column("kwh_initial", sa.Float),
        sa.Column("kwh_final", sa.Float),
        sa.Column("kwh_consumed", sa.Float),
        sa.Column("kwh_cumulative", sa.Float),

        sa.Column("diesel_initial", sa.Float),
        sa.Column("diesel_final", sa.Float),
        sa.Column("diesel_consumed", sa.Float),
        sa.Column("diesel_total", sa.Float),

        sa.Column("remarks", sa.String(500)),
        sa.Column("signature", sa.String(100)),

        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # -----------------------------------
    # dg_250kva_entry_history
    # -----------------------------------
    op.create_table(
        "dg_250kva_entry_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("dg_entry_id", sa.Integer),
        sa.Column("master_ref_id", sa.Integer),

        sa.Column("log_date", sa.Date),
        sa.Column("start_time", sa.Time),
        sa.Column("stop_time", sa.Time),
        sa.Column("run_time", sa.String(20)),

        sa.Column("cumulative", sa.Float),
        sa.Column("hmr", sa.Float),
        sa.Column("battery_voltage", sa.Float),
        sa.Column("lube_oil_pressure", sa.Float),
        sa.Column("rpm", sa.Float),
        sa.Column("electrical_hmr", sa.Float),
        sa.Column("water_temperature", sa.Float),

        sa.Column("voltage_load", sa.Float),
        sa.Column("voltage_ry", sa.Float),
        sa.Column("voltage_yb", sa.Float),
        sa.Column("voltage_br", sa.Float),

        sa.Column("current_r", sa.Float),
        sa.Column("current_y", sa.Float),
        sa.Column("current_b", sa.Float),

        sa.Column("kwh_initial", sa.Float),
        sa.Column("kwh_final", sa.Float),
        sa.Column("kwh_consumed", sa.Float),
        sa.Column("kwh_cumulative", sa.Float),

        sa.Column("diesel_initial", sa.Float),
        sa.Column("diesel_final", sa.Float),
        sa.Column("diesel_consumed", sa.Float),
        sa.Column("diesel_total", sa.Float),

        sa.Column("remarks", sa.String(500)),
        sa.Column("signature", sa.String(100)),

        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table("dg_250kva_entry_history")
    op.drop_table("dg_250kva_entry")
    op.drop_table("dg_250kva_master_history")
    op.drop_table("dg_250kva_master")