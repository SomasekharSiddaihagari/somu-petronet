"""add ms_logbook_id to digital logbook tables

Revision ID: 0da98dff8e6f
Revises: 672788919430
Create Date: 2026-03-02 11:48:24.395512

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0da98dff8e6f'
down_revision: Union[str, Sequence[str], None] = '672788919430'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # -----------------------------------------------------
    # Add column to main tables
    # -----------------------------------------------------
    op.add_column(
        "dkn_digital_logbook",
        sa.Column("ms_logbook_id", sa.Integer(), nullable=True),
    )

    op.add_column(
        "hsn_digital_logbook",
        sa.Column("ms_logbook_id", sa.Integer(), nullable=True),
    )

    op.add_column(
        "mlr_digital_logbook",
        sa.Column("ms_logbook_id", sa.Integer(), nullable=True),
    )

    op.add_column(
        "ner_digital_logbook",
        sa.Column("ms_logbook_id", sa.Integer(), nullable=True),
    )

    # -----------------------------------------------------
    # Add column to history tables
    # -----------------------------------------------------
    op.add_column(
        "dkn_digital_logbook_history",
        sa.Column("ms_logbook_id", sa.Integer(), nullable=True),
    )

    op.add_column(
        "hsn_digital_logbook_history",
        sa.Column("ms_logbook_id", sa.Integer(), nullable=True),
    )

    op.add_column(
        "mlr_digital_logbook_history",
        sa.Column("ms_logbook_id", sa.Integer(), nullable=True),
    )

    op.add_column(
        "ner_digital_logbook_history",
        sa.Column("ms_logbook_id", sa.Integer(), nullable=True),
    )


def downgrade():
    # -----------------------------------------------------
    # Remove column from history tables
    # -----------------------------------------------------
    op.drop_column("ner_digital_logbook_history", "ms_logbook_id")
    op.drop_column("mlr_digital_logbook_history", "ms_logbook_id")
    op.drop_column("hsn_digital_logbook_history", "ms_logbook_id")
    op.drop_column("dkn_digital_logbook_history", "ms_logbook_id")

    # -----------------------------------------------------
    # Remove column from main tables
    # -----------------------------------------------------
    op.drop_column("ner_digital_logbook", "ms_logbook_id")
    op.drop_column("mlr_digital_logbook", "ms_logbook_id")
    op.drop_column("hsn_digital_logbook", "ms_logbook_id")
    op.drop_column("dkn_digital_logbook", "ms_logbook_id")
