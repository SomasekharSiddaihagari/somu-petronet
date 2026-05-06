"""create kptcl tables

Revision ID: acbce9150fc0
Revises: 98d2f34a1acf
Create Date: 2026-01-21 14:52:30.866643

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'acbce9150fc0'
down_revision: Union[str, Sequence[str], None] = '98d2f34a1acf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # =====================================================
    # DKN MASTER
    # =====================================================
    op.create_table(
        "kptcl_dkn_master",
        sa.Column("kptcl_dkn_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("station_name", sa.String(100)),
        sa.Column("station_incharge", sa.String(150)),
        sa.Column("shift", sa.String(20)),
        sa.Column("start_time", sa.Time),
        sa.Column("log_date", sa.Date),
        sa.Column("document_number", sa.String(100)),
        sa.Column("status", sa.String(50)),
        sa.Column("created_by", sa.Integer),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # =====================================================
    # DKN ENTRY
    # =====================================================
    op.create_table(
        "kptcl_dkn_entry",
        sa.Column("kptcl_dkn_entry_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column(
            "master_id",
            sa.Integer,
            sa.ForeignKey("kptcl_dkn_master.kptcl_dkn_id", ondelete="CASCADE"),
        ),
        sa.Column("reading_date", sa.Date),
        sa.Column("reading_time", sa.Time),
        sa.Column("kwh", sa.Numeric(12, 2)),
        sa.Column("kvah", sa.Numeric(12, 2)),
        sa.Column("pf_meter", sa.Numeric(10, 4)),
        sa.Column("calculated_pf_day", sa.String(50)),
        sa.Column("calculated_pf_month", sa.String(50)),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # =====================================================
    # DKN MASTER HISTORY
    # =====================================================
    op.create_table(
        "kptcl_dkn_master_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("kptcl_dkn_id", sa.Integer),
        sa.Column("station_name", sa.String(100)),
        sa.Column("station_incharge", sa.String(150)),
        sa.Column("shift", sa.String(20)),
        sa.Column("start_time", sa.Time),
        sa.Column("log_date", sa.Date),
        sa.Column("document_number", sa.String(100)),
        sa.Column("status", sa.String(50)),
        sa.Column("created_by", sa.Integer),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now()),
    )

    # =====================================================
    # DKN ENTRY HISTORY
    # =====================================================
    op.create_table(
        "kptcl_dkn_entry_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("kptcl_dkn_entry_id", sa.Integer),
        sa.Column("master_id", sa.Integer),
        sa.Column("reading_date", sa.Date),
        sa.Column("reading_time", sa.Time),
        sa.Column("kwh", sa.Numeric(12, 2)),
        sa.Column("kvah", sa.Numeric(12, 2)),
        sa.Column("pf_meter", sa.Numeric(10, 4)),
        sa.Column("calculated_pf_day", sa.String(50)),
        sa.Column("calculated_pf_month", sa.String(50)),
        sa.Column("created_by", sa.Integer),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now()),
    )

    # =====================================================
    # HSN MASTER
    # =====================================================
    op.create_table(
        "kptcl_hsn_master",
        sa.Column("kptcl_hsn_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("station_name", sa.String(100)),
        sa.Column("station_incharge", sa.String(150)),
        sa.Column("shift", sa.String(20)),
        sa.Column("start_time", sa.Time),
        sa.Column("log_date", sa.Date),
        sa.Column("document_number", sa.String(100)),
        sa.Column("status", sa.String(50)),
        sa.Column("billing_kwh_rdg", sa.Numeric(14, 3)),
        sa.Column("billing_kvah_rdg", sa.Numeric(14, 3)),
        sa.Column("monthly_avg_pf", sa.Numeric(10, 4)),
        sa.Column("monthly_avg_kva", sa.Numeric(14, 3)),
        sa.Column("created_by", sa.Integer),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # =====================================================
    # HSN ENTRY
    # =====================================================
    op.create_table(
        "kptcl_hsn_entry",
        sa.Column("kptcl_hsn_entry_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column(
            "master_id",
            sa.Integer,
            sa.ForeignKey("kptcl_hsn_master.kptcl_hsn_id", ondelete="CASCADE"),
        ),
        sa.Column("reading_date", sa.Date),
        sa.Column("reading_time", sa.Time),
        sa.Column("t1c_kwh", sa.Numeric(14, 3)),
        sa.Column("t1c_kvah", sa.Numeric(14, 3)),
        sa.Column("calculated_pf", sa.Numeric(10, 4)),
        sa.Column("t1pr_pf", sa.Numeric(10, 4)),
        sa.Column("t1pr_kva", sa.Numeric(10, 4)),
        sa.Column("initial_final_kwh", sa.Numeric(14, 3)),
        sa.Column("initial_final_kvah", sa.Numeric(14, 3)),
        sa.Column("kwh_kvah", sa.Numeric(14, 3)),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # =====================================================
    # HSN MASTER HISTORY
    # =====================================================
    op.create_table(
        "kptcl_hsn_master_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("kptcl_hsn_id", sa.Integer),
        sa.Column("station_name", sa.String(100)),
        sa.Column("station_incharge", sa.String(150)),
        sa.Column("shift", sa.String(20)),
        sa.Column("start_time", sa.Time),
        sa.Column("log_date", sa.Date),
        sa.Column("document_number", sa.String(100)),
        sa.Column("status", sa.String(50)),
        sa.Column("billing_kwh_rdg", sa.Numeric(14, 3)),
        sa.Column("billing_kvah_rdg", sa.Numeric(14, 3)),
        sa.Column("monthly_avg_pf", sa.Numeric(10, 4)),
        sa.Column("monthly_avg_kva", sa.Numeric(14, 3)),
        sa.Column("created_by", sa.Integer),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now()),
    )

    # =====================================================
    # HSN ENTRY HISTORY
    # =====================================================
    op.create_table(
        "kptcl_hsn_entry_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("kptcl_hsn_entry_id", sa.Integer),
        sa.Column("master_id", sa.Integer),
        sa.Column("reading_date", sa.Date),
        sa.Column("reading_time", sa.Time),
        sa.Column("t1c_kwh", sa.Numeric(14, 3)),
        sa.Column("t1c_kvah", sa.Numeric(14, 3)),
        sa.Column("calculated_pf", sa.Numeric(10, 4)),
        sa.Column("t1pr_pf", sa.Numeric(10, 4)),
        sa.Column("t1pr_kva", sa.Numeric(10, 4)),
        sa.Column("initial_final_kwh", sa.Numeric(14, 3)),
        sa.Column("initial_final_kvah", sa.Numeric(14, 3)),
        sa.Column("kwh_kvah", sa.Numeric(14, 3)),
        sa.Column("created_by", sa.Integer),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now()),
    )

    # =====================================================
    # NER MASTER
    # =====================================================
    op.create_table(
        "kptcl_ner_master",
        sa.Column("kptcl_ner_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("station_name", sa.String(100)),
        sa.Column("station_incharge", sa.String(150)),
        sa.Column("shift", sa.String(20)),
        sa.Column("start_time", sa.Time),
        sa.Column("log_date", sa.Date),
        sa.Column("document_number", sa.String(100)),
        sa.Column("status", sa.String(50)),
        sa.Column("created_by", sa.Integer),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # =====================================================
    # NER ENTRY
    # =====================================================
    op.create_table(
        "kptcl_ner_entry",
        sa.Column("kptcl_ner_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column(
            "master_id",
            sa.Integer,
            sa.ForeignKey("kptcl_ner_master.kptcl_ner_id", ondelete="CASCADE"),
        ),
        sa.Column("reading_date", sa.Date),
        sa.Column("reading_time", sa.Time),
        sa.Column("kwh", sa.Numeric(14, 3)),
        sa.Column("kvah", sa.Numeric(14, 3)),
        sa.Column("pf_meter", sa.Numeric(10, 4)),
        sa.Column("calculated_pf_day", sa.String(50)),
        sa.Column("calculated_pf_month", sa.String(50)),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    # =====================================================
    # NER MASTER HISTORY
    # =====================================================
    op.create_table(
        "kptcl_ner_master_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("kptcl_ner_id", sa.Integer),
        sa.Column("station_name", sa.String(100)),
        sa.Column("station_incharge", sa.String(150)),
        sa.Column("shift", sa.String(20)),
        sa.Column("start_time", sa.Time),
        sa.Column("log_date", sa.Date),
        sa.Column("document_number", sa.String(100)),
        sa.Column("status", sa.String(50)),
        sa.Column("created_by", sa.Integer),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now()),
    )

    # =====================================================
    # NER ENTRY HISTORY
    # =====================================================
    op.create_table(
        "kptcl_ner_entry_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("kptcl_ner_id", sa.Integer),
        sa.Column("master_id", sa.Integer),
        sa.Column("reading_date", sa.Date),
        sa.Column("reading_time", sa.Time),
        sa.Column("kwh", sa.Numeric(14, 3)),
        sa.Column("kvah", sa.Numeric(14, 3)),
        sa.Column("pf_meter", sa.Numeric(10, 4)),
        sa.Column("calculated_pf_day", sa.String(50)),
        sa.Column("calculated_pf_month", sa.String(50)),
        sa.Column("created_by", sa.Integer),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table("kptcl_ner_entry_history")
    op.drop_table("kptcl_ner_master_history")
    op.drop_table("kptcl_ner_entry")
    op.drop_table("kptcl_ner_master")

    op.drop_table("kptcl_hsn_entry_history")
    op.drop_table("kptcl_hsn_master_history")
    op.drop_table("kptcl_hsn_entry")
    op.drop_table("kptcl_hsn_master")

    op.drop_table("kptcl_dkn_entry_history")
    op.drop_table("kptcl_dkn_master_history")
    op.drop_table("kptcl_dkn_entry")
    op.drop_table("kptcl_dkn_master")