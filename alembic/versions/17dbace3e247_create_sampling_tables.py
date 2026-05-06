"""create sampling tables

Revision ID: 17dbace3e247
Revises: 5e38bb16aa83
Create Date: 2026-01-21 16:32:43.673851

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '17dbace3e247'
down_revision: Union[str, Sequence[str], None] = '5e38bb16aa83'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # =====================================================
    # SHIFT TAKEOVER
    # =====================================================
    op.create_table(
        "shift_takeover",
        sa.Column("shift_takeover_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("shift_code", sa.String(20)),
        sa.Column("current_incharge_id", sa.Integer),
        sa.Column("previous_shift_notes", sa.Text),
        sa.Column("takeover_notes", sa.Text),
        sa.Column("is_emergency", sa.Boolean),
        sa.Column("emergency_assigned_to", sa.Integer),
        sa.Column("status", sa.String(50)),
        sa.Column("created_by", sa.Integer),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "shift_takeover_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("shift_takeover_id", sa.Integer),
        sa.Column("shift_code", sa.String(20)),
        sa.Column("current_incharge_id", sa.Integer),
        sa.Column("previous_shift_notes", sa.Text),
        sa.Column("takeover_notes", sa.Text),
        sa.Column("is_emergency", sa.Boolean),
        sa.Column("emergency_assigned_to", sa.Integer),
        sa.Column("status", sa.String(50)),
        sa.Column("created_by", sa.Integer),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now()),
    )

    # =====================================================
    # SHIFT HANDOVER MASTER
    # =====================================================
    op.create_table(
        "shift_handover_master",
        sa.Column("handover_master_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("next_incharge_id", sa.Integer),
        sa.Column("notes_for_next_shift", sa.Text),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # =====================================================
    # SHIFT HANDOVER TASK
    # =====================================================
    op.create_table(
        "shift_handover_task",
        sa.Column("task_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column(
            "handover_id",
            sa.Integer,
            sa.ForeignKey(
                "shift_handover_master.handover_master_id",
                ondelete="CASCADE",
            ),
        ),
        sa.Column("pending_task", sa.String(255)),
        sa.Column("due_date", sa.Date),
        sa.Column("assigned_to", sa.Integer),
        sa.Column("priority", sa.String(20)),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # =====================================================
    # SHIFT HANDOVER MASTER HISTORY
    # =====================================================
    op.create_table(
        "shift_handover_master_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("handover_master_id", sa.Integer),
        sa.Column("next_incharge_id", sa.Integer),
        sa.Column("notes_for_next_shift", sa.Text),
        sa.Column("created_by", sa.Integer),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now()),
    )

    # =====================================================
    # SHIFT HANDOVER TASK HISTORY
    # =====================================================
    op.create_table(
        "shift_handover_task_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("handover_master_id", sa.Integer),
        sa.Column("task_id", sa.Integer),
        sa.Column("pending_task", sa.String(255)),
        sa.Column("due_date", sa.Date),
        sa.Column("assigned_to", sa.Integer),
        sa.Column("priority", sa.String(20)),
        sa.Column("created_by", sa.Integer),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now()),
    )

    # =====================================================
    # DAILY SAMPLING MASTER
    # =====================================================
    op.create_table(
        "daily_sampling_master",
        sa.Column("sampling_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("document_number", sa.String(50)),
        sa.Column("station", sa.String(100)),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("shift", sa.String(20)),
        sa.Column("start_time", sa.Time),
        sa.Column("log_date", sa.Date),
        sa.Column("status", sa.String(30)),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # =====================================================
    # DAILY SAMPLING ENTRY
    # =====================================================
    op.create_table(
        "daily_sampling_entry",
        sa.Column("sampling_entry_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column(
            "master_id",
            sa.Integer,
            sa.ForeignKey(
                "daily_sampling_master.sampling_id",
                ondelete="CASCADE",
            ),
        ),
        sa.Column("sr_no", sa.Integer),
        sa.Column("date", sa.Date),
        sa.Column("sample_time", sa.Time),
        sa.Column("product", sa.String(100)),
        sa.Column("batch_no", sa.String(100)),
        sa.Column("tank", sa.String(100)),
        sa.Column("position", sa.String(100)),
        sa.Column("appearance", sa.String(100)),
        sa.Column("colour", sa.String(100)),
        sa.Column("density", sa.String(50)),
        sa.Column("kinematic_viscosity", sa.String(50)),
        sa.Column("density_at_15c", sa.String(50)),
        sa.Column("qc_density", sa.String(50)),
        sa.Column("difference", sa.String(50)),
        sa.Column("drawn_by", sa.String(100)),
        sa.Column("reason_for_sample_testing", sa.String),
        sa.Column("disposal_date", sa.Date),
        sa.Column("disposed_by", sa.String(100)),
        sa.Column("org_sign", sa.String),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # =====================================================
    # DAILY SAMPLING MASTER HISTORY
    # =====================================================
    op.create_table(
        "daily_sampling_master_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("sampling_id", sa.Integer),
        sa.Column("document_number", sa.String(50)),
        sa.Column("station", sa.String(100)),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("shift", sa.String(20)),
        sa.Column("start_time", sa.Time),
        sa.Column("log_date", sa.Date),
        sa.Column("status", sa.String(30)),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # =====================================================
    # DAILY SAMPLING ENTRY HISTORY
    # =====================================================
    op.create_table(
        "daily_sampling_entry_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("sampling_entry_id", sa.Integer),
        sa.Column("master_id", sa.Integer),
        sa.Column("sr_no", sa.Integer),
        sa.Column("date", sa.Date),
        sa.Column("sample_time", sa.Time),
        sa.Column("product", sa.String(100)),
        sa.Column("batch_no", sa.String(100)),
        sa.Column("tank", sa.String(100)),
        sa.Column("position", sa.String(100)),
        sa.Column("appearance", sa.String(100)),
        sa.Column("colour", sa.String(100)),
        sa.Column("density", sa.String(50)),
        sa.Column("kinematic_viscosity", sa.String(50)),
        sa.Column("density_at_15c", sa.String(50)),
        sa.Column("qc_density", sa.String(50)),
        sa.Column("difference", sa.String(50)),
        sa.Column("drawn_by", sa.String(100)),
        sa.Column("reason_for_sample_testing", sa.String),
        sa.Column("disposal_date", sa.Date),
        sa.Column("disposed_by", sa.String(100)),
        sa.Column("org_sign", sa.String),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table("daily_sampling_entry_history")
    op.drop_table("daily_sampling_master_history")
    op.drop_table("daily_sampling_entry")
    op.drop_table("daily_sampling_master")

    op.drop_table("shift_handover_task_history")
    op.drop_table("shift_handover_master_history")
    op.drop_table("shift_handover_task")
    op.drop_table("shift_handover_master")

    op.drop_table("shift_takeover_history")
    op.drop_table("shift_takeover")