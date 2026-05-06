"""create safety committee incident tables

Revision ID: 7d5e4ee81128
Revises: ab452ebb3ffc
Create Date: 2026-02-26 12:16:01.672561

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7d5e4ee81128'
down_revision: Union[str, Sequence[str], None] = 'ab452ebb3ffc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    # =========================================================
    # TABLE 1: safety_committee_minutes_incidents
    # =========================================================
    op.create_table(
        "safety_committee_minutes_incidents",

        sa.Column("scmi_id", sa.Integer(), primary_key=True, autoincrement=True),

        sa.Column(
            "scmm_id",
            sa.Integer(),
            sa.ForeignKey(
                "safety_committee_minutes.scmm_id",
                ondelete="CASCADE"
            ),
            nullable=False,
        ),

        sa.Column("incident_id", sa.Integer(), nullable=False),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )

    # Optional index for fast joins

    # =========================================================
    # TABLE 2: safety_committee_minutes_incidents_history
    # =========================================================
    op.create_table(
        "safety_committee_minutes_incidents_history",

        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),

        # original incident reference
        sa.Column("scmi_id", sa.Integer(), nullable=True),

        sa.Column("scmm_id", sa.Integer(), nullable=True),

        sa.Column("incident_id", sa.Integer(), nullable=False),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )




def downgrade():

    op.drop_table("safety_committee_minutes_incidents_history")


    op.drop_table("safety_committee_minutes_incidents")