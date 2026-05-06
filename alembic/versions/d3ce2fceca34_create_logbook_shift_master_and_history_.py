"""create logbook shift master and history tables

Revision ID: d3ce2fceca34
Revises: b5a538d5cce3
Create Date: 2026-01-19 21:16:37.445254

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3ce2fceca34'
down_revision: Union[str, Sequence[str], None] = 'b5a538d5cce3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # -------------------- LOGBOOK SHIFT MASTER --------------------
    op.create_table(
        "logbook_shift_master",
        sa.Column("ms_logbook_id", sa.Integer(), primary_key=True, autoincrement=True),

        sa.Column(
            "mlr_logbook_id",
            sa.Integer(),
            sa.ForeignKey("mlr_digital_logbook.mlr_logbook_id"),
            nullable=False,
        ),
        sa.Column(
            "hsn_logbook_id",
            sa.Integer(),
            sa.ForeignKey("hsn_digital_logbook.hsn_logbook_id"),
            nullable=False,
        ),
        sa.Column(
            "dkn_logbook_id",
            sa.Integer(),
            sa.ForeignKey("dkn_digital_logbook.dkn_logbook_id"),
            nullable=False,
        ),

        sa.Column("shift_a", sa.String(length=20)),
        sa.Column("shift_b", sa.String(length=20)),
        sa.Column("shift_c", sa.String(length=20)),

        sa.Column("shift_a_start_time", sa.Time()),
        sa.Column("shift_b_start_time", sa.Time()),
        sa.Column("shift_c_start_time", sa.Time()),

        sa.Column("shift_a_end_time", sa.Time()),
        sa.Column("shift_b_end_time", sa.Time()),
        sa.Column("shift_c_end_time", sa.Time()),

        sa.Column("log_date", sa.Date()),

        sa.Column("shift_a_status", sa.String(length=30)),
        sa.Column("shift_b_status", sa.String(length=30)),
        sa.Column("shift_c_status", sa.String(length=30)),

        sa.Column("shift_a_handover_notes", sa.String(length=500)),
        sa.Column("shift_b_handover_notes", sa.String(length=500)),
        sa.Column("shift_c_handover_notes", sa.String(length=500)),

        sa.Column("shift_a_engineer", sa.String(length=100)),
        sa.Column("shift_b_engineer", sa.String(length=100)),
        sa.Column("shift_c_engineer", sa.String(length=100)),

        sa.Column("created_by", sa.Integer()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("closed_at", sa.DateTime()),
    )

    # -------------------- LOGBOOK SHIFT MASTER HISTORY --------------------
    op.create_table(
        "logbook_shift_master_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),

        sa.Column("ms_logbook_id", sa.Integer()),

        sa.Column("station_name", sa.String(length=100)),
        sa.Column("station_incharge", sa.String(length=100)),

        sa.Column("shift", sa.String(length=20)),
        sa.Column("shift_start_time", sa.Time()),
        sa.Column("shift_end_time", sa.Time()),

        sa.Column("log_date", sa.Date()),
        sa.Column("status", sa.String(length=30)),
        sa.Column("handover_notes", sa.String(length=500)),

        sa.Column("shift_a_technician", sa.String(length=100)),
        sa.Column("shift_a_engineer", sa.String(length=100)),

        sa.Column("shift_b_technician", sa.String(length=100)),
        sa.Column("shift_b_engineer", sa.String(length=100)),

        sa.Column("shift_c_technician", sa.String(length=100)),
        sa.Column("shift_c_engineer", sa.String(length=100)),

        sa.Column("created_by", sa.Integer()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table("logbook_shift_master_history")
    op.drop_table("logbook_shift_master")
