"""update security guard report structure

Revision ID: 39f564e00b48
Revises: 512ebada9dcf
Create Date: 2026-03-17 16:25:57.669200

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '39f564e00b48'
down_revision: Union[str, Sequence[str], None] = '512ebada9dcf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # =========================
    # MAIN TABLE
    # =========================
    with op.batch_alter_table("security_guard_report") as batch_op:

        # DROP GRID FIELDS
        batch_op.drop_column("location_name")
        batch_op.drop_column("guard_shift")
        batch_op.drop_column("security_guard_name")
        batch_op.drop_column("duty_start_time")
        batch_op.drop_column("duty_end_time")
        batch_op.drop_column("battery_cp_volt")
        batch_op.drop_column("battery_tel_volt")
        batch_op.drop_column("power_status")
        batch_op.drop_column("report_details")
        batch_op.drop_column("officer_initials")

        # DROP SIGNATURE FIELDS
        batch_op.drop_column("shift_a_signature")
        batch_op.drop_column("shift_a_name")
        batch_op.drop_column("shift_b_signature")
        batch_op.drop_column("shift_b_name")
        batch_op.drop_column("shift_c_signature")
        batch_op.drop_column("shift_c_name")
        batch_op.drop_column("station_incharge_signature")
        batch_op.drop_column("station_incharge_signed_name")


    # =========================
    # HISTORY TABLE
    # =========================
    with op.batch_alter_table("security_guard_report_history") as batch_op:

        # DROP GRID FIELDS
        batch_op.drop_column("location_name")
        batch_op.drop_column("guard_shift")
        batch_op.drop_column("security_guard_name")
        batch_op.drop_column("duty_start_time")
        batch_op.drop_column("duty_end_time")
        batch_op.drop_column("battery_cp_volt")
        batch_op.drop_column("battery_tel_volt")
        batch_op.drop_column("power_status")
        batch_op.drop_column("report_details")
        batch_op.drop_column("officer_initials")

        # DROP SIGNATURE FIELDS
        batch_op.drop_column("shift_a_signature")
        batch_op.drop_column("shift_a_name")
        batch_op.drop_column("shift_b_signature")
        batch_op.drop_column("shift_b_name")
        batch_op.drop_column("shift_c_signature")
        batch_op.drop_column("shift_c_name")
        batch_op.drop_column("station_incharge_signature")
        batch_op.drop_column("station_incharge_signed_name")

        # ADD COLUMN (if newly introduced)
        batch_op.add_column(sa.Column("security_guard_id", sa.Integer(), nullable=True))


def downgrade():
    # =========================
    # MAIN TABLE ROLLBACK
    # =========================
    with op.batch_alter_table("security_guard_report") as batch_op:

        # ADD BACK GRID FIELDS
        batch_op.add_column(sa.Column("location_name", sa.String(100), nullable=True))
        batch_op.add_column(sa.Column("guard_shift", sa.String(10), nullable=True))
        batch_op.add_column(sa.Column("security_guard_name", sa.String(150), nullable=True))
        batch_op.add_column(sa.Column("duty_start_time", sa.Time(), nullable=True))
        batch_op.add_column(sa.Column("duty_end_time", sa.Time(), nullable=True))
        batch_op.add_column(sa.Column("battery_cp_volt", sa.Numeric(10, 4), nullable=True))
        batch_op.add_column(sa.Column("battery_tel_volt", sa.Numeric(10, 4), nullable=True))
        batch_op.add_column(sa.Column("power_status", sa.String(50), nullable=True))
        batch_op.add_column(sa.Column("report_details", sa.Text(), nullable=True))
        batch_op.add_column(sa.Column("officer_initials", sa.String(50), nullable=True))

        # ADD BACK SIGNATURE FIELDS
        batch_op.add_column(sa.Column("shift_a_signature", sa.String(255), nullable=True))
        batch_op.add_column(sa.Column("shift_a_name", sa.String(100), nullable=True))
        batch_op.add_column(sa.Column("shift_b_signature", sa.String(255), nullable=True))
        batch_op.add_column(sa.Column("shift_b_name", sa.String(100), nullable=True))
        batch_op.add_column(sa.Column("shift_c_signature", sa.String(255), nullable=True))
        batch_op.add_column(sa.Column("shift_c_name", sa.String(100), nullable=True))
        batch_op.add_column(sa.Column("station_incharge_signature", sa.String(255), nullable=True))
        batch_op.add_column(sa.Column("station_incharge_signed_name", sa.String(100), nullable=True))


    # =========================
    # HISTORY TABLE ROLLBACK
    # =========================
    with op.batch_alter_table("security_guard_report_history") as batch_op:

        # ADD BACK GRID FIELDS
        batch_op.add_column(sa.Column("location_name", sa.String(100), nullable=True))
        batch_op.add_column(sa.Column("guard_shift", sa.String(10), nullable=True))
        batch_op.add_column(sa.Column("security_guard_name", sa.String(150), nullable=True))
        batch_op.add_column(sa.Column("duty_start_time", sa.Time(), nullable=True))
        batch_op.add_column(sa.Column("duty_end_time", sa.Time(), nullable=True))
        batch_op.add_column(sa.Column("battery_cp_volt", sa.Numeric(10, 4), nullable=True))
        batch_op.add_column(sa.Column("battery_tel_volt", sa.Numeric(10, 4), nullable=True))
        batch_op.add_column(sa.Column("power_status", sa.String(50), nullable=True))
        batch_op.add_column(sa.Column("report_details", sa.Text(), nullable=True))
        batch_op.add_column(sa.Column("officer_initials", sa.String(50), nullable=True))

        # ADD BACK SIGNATURE FIELDS
        batch_op.add_column(sa.Column("shift_a_signature", sa.String(255), nullable=True))
        batch_op.add_column(sa.Column("shift_a_name", sa.String(100), nullable=True))
        batch_op.add_column(sa.Column("shift_b_signature", sa.String(255), nullable=True))
        batch_op.add_column(sa.Column("shift_b_name", sa.String(100), nullable=True))
        batch_op.add_column(sa.Column("shift_c_signature", sa.String(255), nullable=True))
        batch_op.add_column(sa.Column("shift_c_name", sa.String(100), nullable=True))
        batch_op.add_column(sa.Column("station_incharge_signature", sa.String(255), nullable=True))
        batch_op.add_column(sa.Column("station_incharge_signed_name", sa.String(100), nullable=True))

        # REMOVE ADDED COLUMN
        batch_op.drop_column("security_guard_id")
