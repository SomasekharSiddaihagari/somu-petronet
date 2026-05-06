"""create tank 10kl ffe master and entry tables

Revision ID: a318ca1b4ff4
Revises: 669c858cebfc
Create Date: 2026-01-21 18:22:39.376745

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a318ca1b4ff4'
down_revision: Union[str, Sequence[str], None] = '669c858cebfc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():

    # ------------------------------------
    # tank_10kl_ffe_master
    # ------------------------------------
    op.create_table(
        "tank_10kl_ffe_master",
        sa.Column("tank_ffe_id", sa.Integer, primary_key=True, autoincrement=True),

        sa.Column("station", sa.String(50)),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("shift", sa.String(10)),
        sa.Column("start_time", sa.Time),
        sa.Column("entry_date", sa.Date),
        sa.Column("status", sa.String(20)),

        sa.Column("sign_shift_a", sa.String(100)),
        sa.Column("sign_shift_b", sa.String(100)),
        sa.Column("sign_shift_c", sa.String(100)),
        sa.Column("sign_station_incharge", sa.String(100)),

        sa.Column("name_shift_a", sa.String(100)),
        sa.Column("name_shift_b", sa.String(100)),
        sa.Column("name_shift_c", sa.String(100)),
        sa.Column("name_station_incharge", sa.String(100)),

        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # ------------------------------------
    # tank_10kl_ffe_master_history
    # ------------------------------------
    op.create_table(
        "tank_10kl_ffe_master_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("tank_ffe_id", sa.Integer),

        sa.Column("station", sa.String(50)),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("shift", sa.String(10)),
        sa.Column("start_time", sa.Time),
        sa.Column("entry_date", sa.Date),
        sa.Column("status", sa.String(20)),

        sa.Column("sign_shift_a", sa.String(100)),
        sa.Column("sign_shift_b", sa.String(100)),
        sa.Column("sign_shift_c", sa.String(100)),
        sa.Column("sign_station_incharge", sa.String(100)),

        sa.Column("name_shift_a", sa.String(100)),
        sa.Column("name_shift_b", sa.String(100)),
        sa.Column("name_shift_c", sa.String(100)),
        sa.Column("name_station_incharge", sa.String(100)),

        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # ------------------------------------
    # tank_10kl_ffe_entry
    # ------------------------------------
    op.create_table(
        "tank_10kl_ffe_entry",
        sa.Column("tank_ffe_entry_id", sa.Integer, primary_key=True, autoincrement=True),

        sa.Column(
            "master_id",
            sa.Integer,
            sa.ForeignKey(
                "tank_10kl_ffe_master.tank_ffe_id",
                ondelete="CASCADE"
            ),
        ),

        sa.Column("opening_dip", sa.Float),
        sa.Column("opening_qty", sa.Float),

        sa.Column("qtv_10kl", sa.Float),
        sa.Column("received_250kva", sa.Float),

        sa.Column("fe_01", sa.Float),
        sa.Column("fe_02", sa.Float),
        sa.Column("fe_03", sa.Float),

        sa.Column("sv_08", sa.Float),
        sa.Column("ip", sa.Float),
        sa.Column("sv_09", sa.Float),
        sa.Column("sv_10", sa.Float),

        sa.Column("final_dip", sa.Float),
        sa.Column("final_qty", sa.Float),

        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # ------------------------------------
    # tank_10kl_ffe_entry_history
    # ------------------------------------
    op.create_table(
        "tank_10kl_ffe_entry_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("tank_ffe_entry_id", sa.Integer),
        sa.Column("master_id", sa.Integer),

        sa.Column("opening_dip", sa.Float),
        sa.Column("opening_qty", sa.Float),

        sa.Column("qtv_10kl", sa.Float),
        sa.Column("received_250kva", sa.Float),

        sa.Column("fe_01", sa.Float),
        sa.Column("fe_02", sa.Float),
        sa.Column("fe_03", sa.Float),

        sa.Column("sv_08", sa.Float),
        sa.Column("ip", sa.Float),
        sa.Column("sv_09", sa.Float),
        sa.Column("sv_10", sa.Float),

        sa.Column("final_dip", sa.Float),
        sa.Column("final_qty", sa.Float),

        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table("tank_10kl_ffe_entry_history")
    op.drop_table("tank_10kl_ffe_entry")
    op.drop_table("tank_10kl_ffe_master_history")
    op.drop_table("tank_10kl_ffe_master")