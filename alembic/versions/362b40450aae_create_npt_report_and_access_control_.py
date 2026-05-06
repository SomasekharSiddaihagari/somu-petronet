"""create npt report and access control station tables

Revision ID: 362b40450aae
Revises: 5a8307d1c524
Create Date: 2026-01-22 20:05:40.801998

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '362b40450aae'
down_revision: Union[str, Sequence[str], None] = '5a8307d1c524'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # =====================================================
    # npt_report_master
    # =====================================================
    op.create_table(
        "npt_report_master",
        sa.Column("npt_id", sa.Integer(), primary_key=True, autoincrement=True),

        sa.Column("station", sa.String(100)),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("shift", sa.String(50)),
        sa.Column("start_time", sa.Time()),
        sa.Column("logbook_date", sa.Date()),

        sa.Column("created_by", sa.String(100)),
        sa.Column("created_at", sa.DateTime()),
        sa.Column("updated_at", sa.DateTime()),
    )

    # =====================================================
    # npt_report_master_history
    # =====================================================
    op.create_table(
        "npt_report_master_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("npt_id", sa.Integer()),

        sa.Column("station", sa.String(100)),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("shift", sa.String(50)),
        sa.Column("start_time", sa.Time()),
        sa.Column("logbook_date", sa.Date()),

        sa.Column("created_by", sa.String(100)),
        sa.Column("created_at", sa.DateTime()),
        sa.Column("updated_at", sa.DateTime()),
    )

    # =====================================================
    # npt_report_entry
    # =====================================================
    op.create_table(
        "npt_report_entry",
        sa.Column("npe_id", sa.Integer(), primary_key=True, autoincrement=True),

        sa.Column(
            "master_id",
            sa.Integer(),
            sa.ForeignKey("npt_report_master.npt_id"),
        ),

        sa.Column("patrol_date", sa.Date()),

        sa.Column("start_time", sa.Time()),
        sa.Column("start_point", sa.String(150)),

        sa.Column("end_time", sa.Time()),
        sa.Column("end_point", sa.String(150)),

        sa.Column("team_member", sa.String(150)),

        sa.Column("report_time", sa.Time()),
        sa.Column("point_at_reporting_time", sa.String(255)),

        sa.Column("engg_sign", sa.String(150)),

        sa.Column("remarks", sa.Text()),

        sa.Column("created_by", sa.String(100)),
        sa.Column("created_at", sa.DateTime()),
    )

    # =====================================================
    # npt_report_entry_history
    # =====================================================
    op.create_table(
        "npt_report_entry_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("npe_id", sa.Integer()),
        sa.Column("master_id", sa.Integer()),

        sa.Column("patrol_date", sa.Date()),

        sa.Column("start_time", sa.Time()),
        sa.Column("start_point", sa.String(150)),

        sa.Column("end_time", sa.Time()),
        sa.Column("end_point", sa.String(150)),

        sa.Column("team_member", sa.String(150)),

        sa.Column("report_time", sa.Time()),
        sa.Column("point_at_reporting_time", sa.String(255)),

        sa.Column("engg_sign", sa.String(150)),

        sa.Column("remarks", sa.Text()),

        sa.Column("created_by", sa.String(100)),
        sa.Column("created_at", sa.DateTime()),
    )

    # =====================================================
    # access_control_station
    # (based on your last snippet)
    # =====================================================
   

def downgrade():
    op.drop_table("access_control_station")
    op.drop_table("npt_report_entry_history")
    op.drop_table("npt_report_entry")
    op.drop_table("npt_report_master_history")
    op.drop_table("npt_report_master")