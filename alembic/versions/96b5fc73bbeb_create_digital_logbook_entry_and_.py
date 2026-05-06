"""create digital logbook entry and history tables

Revision ID: 96b5fc73bbeb
Revises: d3ce2fceca34
Create Date: 2026-01-19 21:21:19.299050

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '96b5fc73bbeb'
down_revision: Union[str, Sequence[str], None] = 'd3ce2fceca34'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # ==================== MLR ENTRY ====================
    op.create_table(
        "mlr_digital_logbook_entry",
        sa.Column("mlr_entry_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "mlr_logbook_id",
            sa.Integer(),
            sa.ForeignKey(
                "mlr_digital_logbook.mlr_logbook_id",
                ondelete="CASCADE"
            ),
        ),
        sa.Column("entry_time", sa.Time()),
        sa.Column("location", sa.String(length=100)),
        sa.Column("dkn", sa.String(length=50)),
        sa.Column("hsn", sa.String(length=50)),
        sa.Column("ner", sa.String(length=50)),
        sa.Column("sv1", sa.String(length=50)),
        sa.Column("sv2", sa.String(length=50)),
        sa.Column("created_by", sa.Integer()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "mlr_digital_logbook_entry_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("mlr_entry_id", sa.Integer()),
        sa.Column("mlr_logbook_id", sa.Integer()),
        sa.Column("entry_time", sa.Time()),
        sa.Column("location", sa.String(length=100)),
        sa.Column("dkn", sa.String(length=50)),
        sa.Column("hsn", sa.String(length=50)),
        sa.Column("ner", sa.String(length=50)),
        sa.Column("sv1", sa.String(length=50)),
        sa.Column("sv2", sa.String(length=50)),
        sa.Column("created_by", sa.Integer()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )

    # ==================== HSN ENTRY ====================
    op.create_table(
        "hsn_digital_logbook_entry",
        sa.Column("hsn_entry_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "hsn_logbook_id",
            sa.Integer(),
            sa.ForeignKey(
                "hsn_digital_logbook.hsn_logbook_id",
                ondelete="CASCADE"
            ),
        ),
        sa.Column("entry_time", sa.Time()),
        sa.Column("location", sa.String(length=100)),
        sa.Column("dkn", sa.String(length=50)),
        sa.Column("ner", sa.String(length=50)),
        sa.Column("mlr", sa.String(length=50)),
        sa.Column("sv5", sa.String(length=50)),
        sa.Column("sv6", sa.String(length=50)),
        sa.Column("sv7", sa.String(length=50)),
        sa.Column("created_by", sa.Integer()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "hsn_digital_logbook_entry_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("hsn_entry_id", sa.Integer()),
        sa.Column("hsn_logbook_id", sa.Integer()),
        sa.Column("entry_time", sa.Time()),
        sa.Column("location", sa.String(length=100)),
        sa.Column("dkn", sa.String(length=50)),
        sa.Column("ner", sa.String(length=50)),
        sa.Column("mlr", sa.String(length=50)),
        sa.Column("sv5", sa.String(length=50)),
        sa.Column("sv6", sa.String(length=50)),
        sa.Column("sv7", sa.String(length=50)),
        sa.Column("created_by", sa.Integer()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )

    # ==================== DKN ENTRY ====================
    op.create_table(
        "dkn_digital_logbook_entry",
        sa.Column("dkn_entry_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "logbook_id",
            sa.Integer(),
            sa.ForeignKey(
                "dkn_digital_logbook.dkn_logbook_id",
                ondelete="CASCADE"
            ),
        ),
        sa.Column("entry_time", sa.Time()),
        sa.Column("location", sa.String(length=100)),
        sa.Column("hsn", sa.String(length=50)),
        sa.Column("ner", sa.String(length=50)),
        sa.Column("mlr", sa.String(length=50)),
        sa.Column("svb", sa.String(length=50)),
        sa.Column("ip1", sa.String(length=50)),
        sa.Column("sv9", sa.String(length=50)),
        sa.Column("sv10", sa.String(length=50)),
        sa.Column("created_by", sa.Integer()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "dkn_digital_logbook_entry_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("dkn_entry_id", sa.Integer()),
        sa.Column("logbook_id", sa.Integer()),
        sa.Column("entry_time", sa.Time()),
        sa.Column("location", sa.String(length=100)),
        sa.Column("hsn", sa.String(length=50)),
        sa.Column("ner", sa.String(length=50)),
        sa.Column("mlr", sa.String(length=50)),
        sa.Column("svb", sa.String(length=50)),
        sa.Column("ip1", sa.String(length=50)),
        sa.Column("sv9", sa.String(length=50)),
        sa.Column("sv10", sa.String(length=50)),
        sa.Column("created_by", sa.Integer()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table("dkn_digital_logbook_entry_history")
    op.drop_table("dkn_digital_logbook_entry")
    op.drop_table("hsn_digital_logbook_entry_history")
    op.drop_table("hsn_digital_logbook_entry")
    op.drop_table("mlr_digital_logbook_entry_history")
    op.drop_table("mlr_digital_logbook_entry")