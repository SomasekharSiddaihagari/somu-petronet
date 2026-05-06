"""create digital tank tables

Revision ID: 70e263142a4e
Revises: 0b87f26d6673
Create Date: 2026-01-21 11:56:58.626084

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '70e263142a4e'
down_revision: Union[str, Sequence[str], None] = '0b87f26d6673'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # ============================
    # tank_dip_memo
    # ============================
    op.create_table(
        "tank_dip_memo",
        sa.Column("tank_id", sa.Integer, primary_key=True, autoincrement=True),

        # Header
        sa.Column("document_no", sa.String(100)),
        sa.Column("station_name", sa.String(100)),
        sa.Column("station_incharge", sa.String(100)),
        sa.Column("shift", sa.String(20)),
        sa.Column("start_time", sa.Time),
        sa.Column("status", sa.String(50)),

        # Tank details
        sa.Column("tank_no", sa.String(50)),
        sa.Column("company", sa.String(100)),
        sa.Column("product", sa.String(100)),
        sa.Column("memo_no", sa.String(50)),

        sa.Column("mrpl_batch_no", sa.String(100)),
        sa.Column("pmhbl_batch_no", sa.String(100)),
        sa.Column("before_after_mrpl", sa.String(50)),

        # Date & Time
        sa.Column("dip_time", sa.Time),
        sa.Column("dip_date", sa.Date),

        # DIP Measurements
        sa.Column("ref_height_cm", sa.Float),
        sa.Column("ullage_at_natural", sa.Float),
        sa.Column("gross_dip_cm", sa.Float),
        sa.Column("dip_of_water_mm", sa.Float),

        # Temperature & Density
        sa.Column("temp_top", sa.Float),
        sa.Column("temp_middle", sa.Float),
        sa.Column("temp_bottom", sa.Float),
        sa.Column("temp_average", sa.Float),
        sa.Column("tank_temp", sa.Float),

        sa.Column("density_top", sa.Float),
        sa.Column("density_middle", sa.Float),
        sa.Column("density_bottom", sa.Float),
        sa.Column("density_average", sa.Float),
        sa.Column("density_tank", sa.Float),

        sa.Column("density_at_15c", sa.Float),

        # Settling Time
        sa.Column("settling_time_pmhbl", sa.Float),
        sa.Column("settling_time_hpcl", sa.Float),
        sa.Column("settling_time_bpcl_iocl", sa.Float),

        # Footer
        sa.Column("entered_by_name", sa.String(100)),
        sa.Column("entered_date", sa.Date),

        sa.Column("created_by", sa.Integer),
        sa.Column(
            "created_at",
            sa.DateTime,
            server_default=sa.func.now()
        ),
    )

    # ============================
    # tank_dip_memo_history
    # ============================
    op.create_table(
        "tank_dip_memo_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),

        sa.Column("tank_id", sa.Integer),

        sa.Column("document_no", sa.String(100)),
        sa.Column("station_name", sa.String(100)),
        sa.Column("station_incharge", sa.String(100)),
        sa.Column("shift", sa.String(20)),
        sa.Column("start_time", sa.Time),
        sa.Column("status", sa.String(50)),

        sa.Column("tank_no", sa.String(50)),
        sa.Column("company", sa.String(100)),
        sa.Column("product", sa.String(100)),
        sa.Column("memo_no", sa.String(50)),

        sa.Column("mrpl_batch_no", sa.String(100)),
        sa.Column("pmhbl_batch_no", sa.String(100)),
        sa.Column("before_after_mrpl", sa.String(50)),

        sa.Column("dip_time", sa.Time),
        sa.Column("dip_date", sa.Date),

        sa.Column("ref_height_cm", sa.Float),
        sa.Column("ullage_at_natural", sa.Float),
        sa.Column("gross_dip_cm", sa.Float),
        sa.Column("dip_of_water_mm", sa.Float),

        sa.Column("temp_top", sa.Float),
        sa.Column("temp_middle", sa.Float),
        sa.Column("temp_bottom", sa.Float),
        sa.Column("temp_average", sa.Float),
        sa.Column("tank_temp", sa.Float),

        sa.Column("density_top", sa.Float),
        sa.Column("density_middle", sa.Float),
        sa.Column("density_bottom", sa.Float),
        sa.Column("density_average", sa.Float),
        sa.Column("density_tank", sa.Float),

        sa.Column("density_at_15c", sa.Float),

        sa.Column("settling_time_pmhbl", sa.Float),
        sa.Column("settling_time_hpcl", sa.Float),
        sa.Column("settling_time_bpcl_iocl", sa.Float),

        sa.Column("entered_by_name", sa.String(100)),
        sa.Column("entered_date", sa.Date),

        sa.Column("created_by", sa.Integer),
        sa.Column(
            "updated_at",
            sa.DateTime,
            server_default=sa.func.now()
        ),
    )


def downgrade():
    op.drop_table("tank_dip_memo_history")
    op.drop_table("tank_dip_memo")