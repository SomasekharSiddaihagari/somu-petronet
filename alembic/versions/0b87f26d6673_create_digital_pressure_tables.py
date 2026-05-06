"""create digital pressure tables

Revision ID: 0b87f26d6673
Revises: 0898c826a9f6
Create Date: 2026-01-21 11:35:50.040724

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0b87f26d6673'
down_revision: Union[str, Sequence[str], None] = '0898c826a9f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ============================
    # pressure_log_master
    # ============================
    op.create_table(
        "pressure_log_master",
        sa.Column("pressure_id", sa.Integer, primary_key=True, autoincrement=True),

        sa.Column("logbook_ref_no", sa.String(100)),
        sa.Column("station_name", sa.String(100)),
        sa.Column("station_incharge", sa.String(100)),

        sa.Column("shift", sa.String(10)),
        sa.Column("log_date", sa.Date),
        sa.Column("start_time", sa.Time),

        sa.Column("shift_a_technician_name", sa.String(100)),
        sa.Column("shift_a_technician_signature", sa.String(255)),
        sa.Column("shift_a_engineer_name", sa.String(100)),
        sa.Column("shift_a_engineer_signature", sa.String(255)),

        sa.Column("shift_b_technician_name", sa.String(100)),
        sa.Column("shift_b_technician_signature", sa.String(255)),
        sa.Column("shift_b_engineer_name", sa.String(100)),
        sa.Column("shift_b_engineer_signature", sa.String(255)),

        sa.Column("shift_c_technician_name", sa.String(100)),
        sa.Column("shift_c_technician_signature", sa.String(255)),
        sa.Column("shift_c_engineer_name", sa.String(100)),
        sa.Column("shift_c_engineer_signature", sa.String(255)),

        sa.Column("is_closed", sa.Boolean),
        sa.Column("created_by", sa.Integer),

        sa.Column(
            "created_at",
            sa.DateTime,
            server_default=sa.func.now()
        ),
    )

    # ============================
    # pressure_log_entry
    # ============================
    op.create_table(
        "pressure_log_entry",
        sa.Column("pressure_entry_id", sa.Integer, primary_key=True, autoincrement=True),

        sa.Column(
            "pressure_id",
            sa.Integer,
            sa.ForeignKey(
                "pressure_log_master.pressure_id",
                ondelete="CASCADE"
            ),
        ),

        sa.Column("entry_date", sa.Date),
        sa.Column("entry_time", sa.Time),

        sa.Column("mangalore", sa.String(50)),
        sa.Column("sv1", sa.String(50)),
        sa.Column("sv2", sa.String(50)),
        sa.Column("sv3", sa.String(50)),

        sa.Column("neriya", sa.String(50)),
        sa.Column("sv4", sa.String(50)),
        sa.Column("sv5", sa.String(50)),

        sa.Column("hassan", sa.String(50)),
        sa.Column("sv6", sa.String(50)),
        sa.Column("sv7", sa.String(50)),
        sa.Column("sv8", sa.String(50)),

        sa.Column("ip", sa.String(50)),
        sa.Column("sv9", sa.String(50)),
        sa.Column("sv10", sa.String(50)),

        sa.Column("bangalore", sa.String(50)),

        sa.Column(
            "created_at",
            sa.DateTime,
            server_default=sa.func.now()
        ),
    )

    # ============================
    # pressure_log_master_history
    # ============================
    op.create_table(
        "pressure_log_master_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),

        sa.Column("pressure_id", sa.Integer),

        sa.Column("logbook_ref_no", sa.String(100)),
        sa.Column("station_name", sa.String(100)),
        sa.Column("station_incharge", sa.String(100)),

        sa.Column("shift", sa.String(10)),
        sa.Column("log_date", sa.Date),
        sa.Column("start_time", sa.Time),

        sa.Column("shift_a_technician_name", sa.String(100)),
        sa.Column("shift_a_technician_signature", sa.String(255)),
        sa.Column("shift_a_engineer_name", sa.String(100)),
        sa.Column("shift_a_engineer_signature", sa.String(255)),

        sa.Column("shift_b_technician_name", sa.String(100)),
        sa.Column("shift_b_technician_signature", sa.String(255)),
        sa.Column("shift_b_engineer_name", sa.String(100)),
        sa.Column("shift_b_engineer_signature", sa.String(255)),

        sa.Column("shift_c_technician_name", sa.String(100)),
        sa.Column("shift_c_technician_signature", sa.String(255)),
        sa.Column("shift_c_engineer_name", sa.String(100)),
        sa.Column("shift_c_engineer_signature", sa.String(255)),

        sa.Column("is_closed", sa.Boolean),
        sa.Column("created_by", sa.Integer),

        sa.Column(
            "updated_at",
            sa.DateTime,
            server_default=sa.func.now()
        ),
    )

    # ============================
    # pressure_log_entry_history
    # ============================
    op.create_table(
        "pressure_log_entry_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),

        sa.Column("pressure_entry_id", sa.Integer),
        sa.Column("pressure_id", sa.Integer),

        sa.Column("entry_date", sa.Date),
        sa.Column("entry_time", sa.Time),

        sa.Column("mangalore", sa.String(50)),
        sa.Column("sv1", sa.String(50)),
        sa.Column("sv2", sa.String(50)),
        sa.Column("sv3", sa.String(50)),

        sa.Column("neriya", sa.String(50)),
        sa.Column("sv4", sa.String(50)),
        sa.Column("sv5", sa.String(50)),

        sa.Column("hassan", sa.String(50)),
        sa.Column("sv6", sa.String(50)),
        sa.Column("sv7", sa.String(50)),
        sa.Column("sv8", sa.String(50)),

        sa.Column("ip", sa.String(50)),
        sa.Column("sv9", sa.String(50)),
        sa.Column("sv10", sa.String(50)),

        sa.Column("bangalore", sa.String(50)),

        sa.Column("created_by", sa.Integer),

        sa.Column(
            "updated_at",
            sa.DateTime,
            server_default=sa.func.now()
        ),
    )


def downgrade():
    op.drop_table("pressure_log_entry_history")
    op.drop_table("pressure_log_master_history")
    op.drop_table("pressure_log_entry")
    op.drop_table("pressure_log_master")