"""create geo fencing

Revision ID: c52cfa610fa0
Revises: 4da73fd1a740
Create Date: 2026-01-22 12:57:00.046650
"""

import enum
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c52cfa610fa0'
down_revision: Union[str, Sequence[str], None] = '4da73fd1a740'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# ---------- ENUM ----------
class AccessTypeEnum(str, enum.Enum):
    IP = "IP"
    GEO = "GEO"
    APPROVAL = "APPROVAL"


def upgrade():

    # =========================
    # SHIFT
    # =========================
    op.create_table(
        "shift",
        sa.Column("shift_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("shift_name", sa.String(50), nullable=False, unique=True),
        sa.Column("start_time", sa.Time, nullable=False),
        sa.Column("end_time", sa.Time, nullable=False),
    )

    op.create_table(
        "shift_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("shift_id", sa.Integer, nullable=True),
        sa.Column("shift_name", sa.String(50), nullable=False, unique=True),
        sa.Column("start_time", sa.Time, nullable=False),
        sa.Column("end_time", sa.Time, nullable=False),
    )

    # =========================
    # ACCESS CONTROL STATION
    # =========================
    op.create_table(
        "access_control_station",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("station_id", sa.Integer, nullable=False, unique=True),
        sa.Column("station_name", sa.String(150)),
        sa.Column("ip_from", sa.String(45)),
        sa.Column("ip_to", sa.String(45)),
        sa.Column("lat", sa.Float),
        sa.Column("lon", sa.Float),
        sa.Column("radius", sa.Float),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    op.create_table(
        "access_control_station_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("id", sa.Integer),
        sa.Column("station_id", sa.Integer, nullable=False, unique=True),
        sa.Column("station_name", sa.String(150)),
        sa.Column("ip_from", sa.String(45)),
        sa.Column("ip_to", sa.String(45)),
        sa.Column("lat", sa.Float),
        sa.Column("lon", sa.Float),
        sa.Column("radius", sa.Float),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    # =========================
    # LOCATION ACCESS APPROVAL
    # =========================
    op.create_table(
        "location_access_approval",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("requested_station_id", sa.Integer, sa.ForeignKey("station.station_id"), nullable=False),
        sa.Column("requested_by_user_id", sa.Integer, sa.ForeignKey("users.user_id"), nullable=False),
        sa.Column("approved_by_user_id", sa.Integer, sa.ForeignKey("users.user_id"), nullable=False),
        sa.Column("approved_by_station_id", sa.Integer, sa.ForeignKey("station.station_id"), nullable=False),
        sa.Column("approved_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "approved_by_station_id <> requested_station_id",
            name="chk_cross_station_approval_only"
        ),
    )

    op.create_table(
        "location_access_approval_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("id", sa.Integer),
        sa.Column("requested_station_id", sa.Integer, nullable=False),
        sa.Column("requested_by_user_id", sa.Integer, nullable=False),
        sa.Column("approved_by_user_id", sa.Integer, nullable=False),
        sa.Column("approved_by_station_id", sa.Integer, nullable=False),
        sa.Column("approved_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "approved_by_station_id <> requested_station_id",
            name="chk_cross_station_approval_only"
        ),
    )

    # =========================
    # LOCATION ACCESS TOKEN
    # =========================
    # IMPORTANT: reuse existing enum, DO NOT create it
    access_type_enum = sa.Enum(
        AccessTypeEnum,
        name="accesstypeenum",
        create_type=False
    )
    op.create_table(
        "location_access_token",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.user_id"), nullable=False),
        sa.Column("station_id", sa.Integer, sa.ForeignKey("station.station_id"), nullable=False),
        sa.Column("token", sa.String(128), nullable=False, unique=True),
        sa.Column("access_type", access_type_enum, nullable=False),
        sa.Column("ip_address", sa.String(45), nullable=False),
        sa.Column("latitude", sa.Float, nullable=False),
        sa.Column("longitude", sa.Float, nullable=False),
        sa.Column("approved_by_user_id", sa.Integer, sa.ForeignKey("users.user_id")),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint(
            "user_id", "station_id", "is_active",
            name="uq_lat_one_active_token_per_station"
        ),
    )

    op.create_table(
        "location_access_token_history",
        sa.Column("historyid", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column("station_id", sa.Integer, nullable=False),
        sa.Column("token", sa.String(128), nullable=False, unique=True),
        sa.Column("access_type", access_type_enum, nullable=False),
        sa.Column("ip_address", sa.String(45), nullable=False),
        sa.Column("latitude", sa.Float, nullable=False),
        sa.Column("longitude", sa.Float, nullable=False),
        sa.Column("approved_by_user_id", sa.Integer),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint(
            "user_id", "station_id", "is_active",
            name="uq_lat_hist_one_active_token_per_station"
        ),
    )

    # =========================
    # SHIFT HANDOVER LOG
    # =========================
    op.create_table(
        "shift_handover_log",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("station_id", sa.Integer, sa.ForeignKey("station.station_id"), nullable=False),
        sa.Column("shift_id", sa.Integer, sa.ForeignKey("shift.shift_id"), nullable=False),
        sa.Column("from_user_id", sa.Integer, sa.ForeignKey("users.user_id"), nullable=False),
        sa.Column("to_user_id", sa.Integer, sa.ForeignKey("users.user_id"), nullable=False),
        sa.Column("event_type", sa.String(50), nullable=False),
        sa.Column("event_time", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("remarks", sa.String(255)),
    )

    op.create_table(
        "shift_handover_log_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("id", sa.Integer),
        sa.Column("station_id", sa.Integer, nullable=False),
        sa.Column("shift_id", sa.Integer, nullable=False),
        sa.Column("from_user_id", sa.Integer, nullable=False),
        sa.Column("to_user_id", sa.Integer, nullable=False),
        sa.Column("event_type", sa.String(50), nullable=False),
        sa.Column("event_time", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("remarks", sa.String(255)),
    )

    # =========================
    # STATION SHIFT INCHARGE
    # =========================
    op.create_table(
        "station_shift_incharge",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("station_id", sa.Integer, sa.ForeignKey("station.station_id"), nullable=False),
        sa.Column("shift_id", sa.Integer, sa.ForeignKey("shift.shift_id"), nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.user_id"), nullable=False),
        sa.Column("responsibility_from", sa.DateTime(timezone=True), nullable=False),
        sa.Column("responsibility_to", sa.DateTime(timezone=True)),
        sa.Column("handover_requested_at", sa.DateTime(timezone=True)),
        sa.Column("handover_accepted_at", sa.DateTime(timezone=True)),
        sa.Column("handover_to_user_id", sa.Integer, sa.ForeignKey("users.user_id")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "station_shift_incharge_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("id", sa.Integer),
        sa.Column("station_id", sa.Integer, nullable=False),
        sa.Column("shift_id", sa.Integer, nullable=False),
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column("responsibility_from", sa.DateTime(timezone=True), nullable=False),
        sa.Column("responsibility_to", sa.DateTime(timezone=True)),
        sa.Column("handover_requested_at", sa.DateTime(timezone=True)),
        sa.Column("handover_accepted_at", sa.DateTime(timezone=True)),
        sa.Column("handover_to_user_id", sa.Integer),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
