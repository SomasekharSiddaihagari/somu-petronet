"""create mfm accounting hsn and dkn tables

Revision ID: 669c858cebfc
Revises: 17dbace3e247
Create Date: 2026-01-21 18:12:30.996404

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '669c858cebfc'
down_revision: Union[str, Sequence[str], None] = '17dbace3e247'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    # -------------------------------
    # mfm_accounting_hsn
    # -------------------------------
    op.create_table(
        "mfm_accounting_hsn",
        sa.Column("mfm_acc_hsn_id", sa.Integer, primary_key=True, autoincrement=True),

        sa.Column("station", sa.String(50)),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("shift", sa.String(10)),
        sa.Column("start_time", sa.Time),
        sa.Column("status", sa.String(20)),
        sa.Column("document_number", sa.String(50)),
        sa.Column("otr_no", sa.String(50)),
        sa.Column("mfm_number", sa.String(50)),
        sa.Column("receiving_company", sa.String(50)),
        sa.Column("entry_date", sa.Date),

        sa.Column("tank_no", sa.String(50)),
        sa.Column("product", sa.String(50)),
        sa.Column("mrpl_batch_no", sa.String(50)),
        sa.Column("pmhbl_batch_no", sa.String(50)),

        sa.Column("open_vol_kl_amb", sa.Float),
        sa.Column("open_vol_kl_15c", sa.Float),
        sa.Column("open_mass_mt", sa.Float),
        sa.Column("open_density_amb", sa.Float),
        sa.Column("open_density_15c", sa.Float),
        sa.Column("open_temp", sa.Float),
        sa.Column("open_date", sa.Date),
        sa.Column("open_time", sa.Time),

        sa.Column("close_vol_kl_amb", sa.Float),
        sa.Column("close_vol_kl_15c", sa.Float),
        sa.Column("close_mass_mt", sa.Float),
        sa.Column("close_density_amb", sa.Float),
        sa.Column("close_density_15c", sa.Float),
        sa.Column("close_temp", sa.Float),
        sa.Column("close_date", sa.Date),
        sa.Column("close_time", sa.Time),

        sa.Column("remarks", sa.String(500)),

        sa.Column("sign_open_pmhbl", sa.String(100)),
        sa.Column("sign_open_hpcl", sa.String(100)),
        sa.Column("sign_close_pmhbl", sa.String(100)),
        sa.Column("sign_close_hpcl", sa.String(100)),

        sa.Column("name_open_pmhbl", sa.String(100)),
        sa.Column("name_open_hpcl", sa.String(100)),
        sa.Column("name_close_pmhbl", sa.String(100)),
        sa.Column("name_close_hpcl", sa.String(100)),

        sa.Column("quality_tranfered_amb_total", sa.Float),
        sa.Column("quality_tranfered_15c_total", sa.Float),
        sa.Column("quality_tranfered_mass_total", sa.Float),

        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # -------------------------------
    # mfm_accounting_hsn_history
    # -------------------------------
    op.create_table(
        "mfm_accounting_hsn_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("mfm_acc_hsn_id", sa.Integer),

        sa.Column("document_number", sa.String(50)),
        sa.Column("station", sa.String(50)),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("shift", sa.String(10)),
        sa.Column("start_time", sa.Time),
        sa.Column("status", sa.String(20)),

        sa.Column("otr_no", sa.String(50)),
        sa.Column("mfm_number", sa.String(50)),
        sa.Column("receiving_company", sa.String(50)),
        sa.Column("entry_date", sa.Date),

        sa.Column("tank_no", sa.String(50)),
        sa.Column("product", sa.String(50)),
        sa.Column("mrpl_batch_no", sa.String(50)),
        sa.Column("pmhbl_batch_no", sa.String(50)),

        sa.Column("open_vol_kl_amb", sa.Float),
        sa.Column("open_vol_kl_15c", sa.Float),
        sa.Column("open_mass_mt", sa.Float),
        sa.Column("open_density_amb", sa.Float),
        sa.Column("open_density_15c", sa.Float),
        sa.Column("open_temp", sa.Float),
        sa.Column("open_date", sa.Date),
        sa.Column("open_time", sa.Time),

        sa.Column("close_vol_kl_amb", sa.Float),
        sa.Column("close_vol_kl_15c", sa.Float),
        sa.Column("close_mass_mt", sa.Float),
        sa.Column("close_density_amb", sa.Float),
        sa.Column("close_density_15c", sa.Float),
        sa.Column("close_temp", sa.Float),
        sa.Column("close_date", sa.Date),
        sa.Column("close_time", sa.Time),

        sa.Column("remarks", sa.String(500)),

        sa.Column("sign_open_pmhbl", sa.String(100)),
        sa.Column("sign_open_hpcl", sa.String(100)),
        sa.Column("sign_close_pmhbl", sa.String(100)),
        sa.Column("sign_close_hpcl", sa.String(100)),

        sa.Column("name_open_pmhbl", sa.String(100)),
        sa.Column("name_open_hpcl", sa.String(100)),
        sa.Column("name_close_pmhbl", sa.String(100)),
        sa.Column("name_close_hpcl", sa.String(100)),

        sa.Column("quality_tranfered_amb_total", sa.Float),
        sa.Column("quality_tranfered_15c_total", sa.Float),
        sa.Column("quality_tranfered_mass_total", sa.Float),

        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # -------------------------------
    # mfm_accounting_dkn
    # -------------------------------
    op.create_table(
        "mfm_accounting_dkn",
        sa.Column("mfm_acc_dkn_id", sa.Integer, primary_key=True, autoincrement=True),

        sa.Column("station", sa.String(100)),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("shift", sa.String(20)),
        sa.Column("start_time", sa.Time),
        sa.Column("document_number", sa.String(50)),
        sa.Column("otr_no", sa.String(50)),
        sa.Column("mfm_number", sa.String(50)),
        sa.Column("receiving_company", sa.String(50)),
        sa.Column("log_date", sa.Date),

        sa.Column("tank_no", sa.String(50)),
        sa.Column("product", sa.String(50)),
        sa.Column("mrpl_batch_no", sa.String(50)),
        sa.Column("pmhbl_batch_no", sa.String(50)),

        sa.Column("opening_vol_kl_amb", sa.Numeric(12, 3)),
        sa.Column("opening_vol_kl_15c", sa.Numeric(12, 3)),
        sa.Column("opening_mass_mt", sa.Numeric(12, 3)),
        sa.Column("opening_weighted_amb_density", sa.Numeric(10, 4)),
        sa.Column("opening_weighted_temp", sa.Numeric(6, 2)),
        sa.Column("opening_weighted_15c_density", sa.Numeric(10, 4)),
        sa.Column("opening_date", sa.Date),
        sa.Column("opening_time", sa.Time),

        sa.Column("closing_vol_kl_amb", sa.Numeric(12, 3)),
        sa.Column("closing_vol_kl_15c", sa.Numeric(12, 3)),
        sa.Column("closing_mass_mt", sa.Numeric(12, 3)),
        sa.Column("closing_weighted_amb_density", sa.Numeric(10, 4)),
        sa.Column("closing_weighted_temp", sa.Numeric(6, 2)),
        sa.Column("closing_weighted_15c_density", sa.Numeric(10, 4)),
        sa.Column("closing_date", sa.Date),
        sa.Column("closing_time", sa.Time),

        sa.Column("qty_transferred_vol_kl", sa.Numeric(12, 3)),
        sa.Column("qty_transferred_mass_mt", sa.Numeric(12, 3)),
        sa.Column("qty_transferred_15c_total", sa.Numeric(12, 3)),
        sa.Column("qty_transferred_mass_total", sa.Numeric(12, 3)),
        sa.Column("qty_transferred_amb_total", sa.Numeric(12, 3)),

        sa.Column("remarks", sa.String),
        sa.Column("opening_pmhbl_signature", sa.String),
        sa.Column("opening_mrpl_signature", sa.String),
        sa.Column("closing_pmhbl_signature", sa.String),
        sa.Column("closing_mrpl_signature", sa.String),

        sa.Column("name_open_pmhbl", sa.String(100)),
        sa.Column("name_open_hpcl", sa.String(100)),
        sa.Column("name_close_pmhbl", sa.String(100)),
        sa.Column("name_close_hpcl", sa.String(100)),

        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # -------------------------------
    # mfm_accounting_dkn_history
    # -------------------------------
    op.create_table(
        "mfm_accounting_dkn_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("mfm_acc_dkn_id", sa.Integer),

        sa.Column("station", sa.String(100)),
        sa.Column("station_in_charge", sa.String(100)),
        sa.Column("shift", sa.String(20)),
        sa.Column("start_time", sa.Time),
        sa.Column("document_number", sa.String(50)),
        sa.Column("otr_no", sa.String(50)),
        sa.Column("mfm_number", sa.String(50)),
        sa.Column("receiving_company", sa.String(50)),
        sa.Column("log_date", sa.Date),

        sa.Column("tank_no", sa.String(50)),
        sa.Column("product", sa.String(50)),
        sa.Column("mrpl_batch_no", sa.String(50)),
        sa.Column("pmhbl_batch_no", sa.String(50)),

        sa.Column("opening_vol_kl_amb", sa.Numeric(12, 3)),
        sa.Column("opening_vol_kl_15c", sa.Numeric(12, 3)),
        sa.Column("opening_mass_mt", sa.Numeric(12, 3)),
        sa.Column("opening_weighted_amb_density", sa.Numeric(10, 4)),
        sa.Column("opening_weighted_temp", sa.Numeric(6, 2)),
        sa.Column("opening_weighted_15c_density", sa.Numeric(10, 4)),
        sa.Column("opening_date", sa.Date),
        sa.Column("opening_time", sa.Time),

        sa.Column("closing_vol_kl_amb", sa.Numeric(12, 3)),
        sa.Column("closing_vol_kl_15c", sa.Numeric(12, 3)),
        sa.Column("closing_mass_mt", sa.Numeric(12, 3)),
        sa.Column("closing_weighted_amb_density", sa.Numeric(10, 4)),
        sa.Column("closing_weighted_temp", sa.Numeric(6, 2)),
        sa.Column("closing_weighted_15c_density", sa.Numeric(10, 4)),
        sa.Column("closing_date", sa.Date),
        sa.Column("closing_time", sa.Time),

        sa.Column("qty_transferred_vol_kl", sa.Numeric(12, 3)),
        sa.Column("qty_transferred_mass_mt", sa.Numeric(12, 3)),
        sa.Column("qty_transferred_15c_total", sa.Numeric(12, 3)),
        sa.Column("qty_transferred_mass_total", sa.Numeric(12, 3)),
        sa.Column("qty_transferred_amb_total", sa.Numeric(12, 3)),

        sa.Column("remarks", sa.String),
        sa.Column("opening_pmhbl_signature", sa.String),
        sa.Column("opening_mrpl_signature", sa.String),
        sa.Column("closing_pmhbl_signature", sa.String),
        sa.Column("closing_mrpl_signature", sa.String),

        sa.Column("name_open_pmhbl", sa.String(100)),
        sa.Column("name_open_hpcl", sa.String(100)),
        sa.Column("name_close_pmhbl", sa.String(100)),
        sa.Column("name_close_hpcl", sa.String(100)),

        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table("mfm_accounting_dkn_history")
    op.drop_table("mfm_accounting_dkn")
    op.drop_table("mfm_accounting_hsn_history")
    op.drop_table("mfm_accounting_hsn")