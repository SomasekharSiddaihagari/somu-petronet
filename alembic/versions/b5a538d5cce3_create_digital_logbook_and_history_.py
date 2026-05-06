"""create digital logbook and history tables

Revision ID: b5a538d5cce3
Revises: a6f81c4827de
Create Date: 2026-01-19 21:14:43.646281

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b5a538d5cce3'
down_revision: Union[str, Sequence[str], None] = 'a6f81c4827de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # -------------------- DKN --------------------
    op.create_table(
        "dkn_digital_logbook",
        sa.Column("dkn_logbook_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("station", sa.String(length=100)),
        sa.Column("station_in_charge", sa.String(length=100)),
        sa.Column("shift", sa.String(length=20)),
        sa.Column("logbook_ref_no", sa.String(length=50)),
        sa.Column("log_date", sa.Date()),
        sa.Column("start_time", sa.Time()),
        sa.Column("handed_over_by", sa.String(length=100)),
        sa.Column("taken_over_by", sa.String(length=100)),
        sa.Column("is_shift_closed", sa.Boolean()),
        sa.Column("created_by", sa.Integer()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "dkn_digital_logbook_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("logbook_id", sa.Integer()),
        sa.Column("station", sa.String(length=100)),
        sa.Column("station_in_charge", sa.String(length=100)),
        sa.Column("shift", sa.String(length=20)),
        sa.Column("log_date", sa.Date()),
        sa.Column("start_time", sa.Time()),
        sa.Column("handed_over_by", sa.String(length=100)),
        sa.Column("taken_over_by", sa.String(length=100)),
        sa.Column("is_shift_closed", sa.Boolean()),
        sa.Column("created_by", sa.Integer()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    # -------------------- HSN --------------------
    op.create_table(
        "hsn_digital_logbook",
        sa.Column("hsn_logbook_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("logbook_ref_no", sa.String(length=50)),
        sa.Column("station", sa.String(length=100)),
        sa.Column("station_in_charge", sa.String(length=100)),
        sa.Column("shift", sa.String(length=20)),
        sa.Column("log_date", sa.Date()),
        sa.Column("start_time", sa.Time()),
        sa.Column("handed_over_by", sa.String(length=100)),
        sa.Column("taken_over_by", sa.String(length=100)),
        sa.Column("is_shift_closed", sa.Boolean()),
        sa.Column("created_by", sa.Integer()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "hsn_digital_logbook_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("hsn_logbook_id", sa.Integer()),
        sa.Column("logbook_ref_no", sa.String(length=50)),
        sa.Column("station", sa.String(length=100)),
        sa.Column("station_in_charge", sa.String(length=100)),
        sa.Column("shift", sa.String(length=20)),
        sa.Column("log_date", sa.Date()),
        sa.Column("start_time", sa.Time()),
        sa.Column("handed_over_by", sa.String(length=100)),
        sa.Column("taken_over_by", sa.String(length=100)),
        sa.Column("is_shift_closed", sa.Boolean()),
        sa.Column("created_by", sa.Integer()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )

    # -------------------- MLR --------------------
    op.create_table(
        "mlr_digital_logbook",
        sa.Column("mlr_logbook_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("logbook_ref_no", sa.String(length=50)),
        sa.Column("station", sa.String(length=100)),
        sa.Column("station_in_charge", sa.String(length=100)),
        sa.Column("shift", sa.String(length=20)),
        sa.Column("log_date", sa.Date()),
        sa.Column("start_time", sa.Time()),
        sa.Column("handed_over_by", sa.String(length=100)),
        sa.Column("taken_over_by", sa.String(length=100)),
        sa.Column("is_shift_closed", sa.Boolean()),
        sa.Column("created_by", sa.Integer()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "mlr_digital_logbook_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("mlr_logbook_id", sa.Integer()),
        sa.Column("logbook_ref_no", sa.String(length=50)),
        sa.Column("station", sa.String(length=100)),
        sa.Column("station_in_charge", sa.String(length=100)),
        sa.Column("shift", sa.String(length=20)),
        sa.Column("log_date", sa.Date()),
        sa.Column("start_time", sa.Time()),
        sa.Column("handed_over_by", sa.String(length=100)),
        sa.Column("taken_over_by", sa.String(length=100)),
        sa.Column("is_shift_closed", sa.Boolean()),
        sa.Column("created_by", sa.Integer()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table("mlr_digital_logbook_history")
    op.drop_table("mlr_digital_logbook")
    op.drop_table("hsn_digital_logbook_history")
    op.drop_table("hsn_digital_logbook")
    op.drop_table("dkn_digital_logbook_history")
    op.drop_table("dkn_digital_logbook")