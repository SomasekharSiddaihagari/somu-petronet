"""create incident investigation team tables

Revision ID: 67931d3c3b2e
Revises: d83c147ad579
Create Date: 2026-02-02 12:49:37.043014

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67931d3c3b2e'
down_revision: Union[str, Sequence[str], None] = 'd83c147ad579'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # --------------------------------------------
    # incident_investigation_team
    # --------------------------------------------
    op.create_table(
        "incident_investigation_team",
        sa.Column("iit_id", sa.Integer(), primary_key=True, autoincrement=True),

        sa.Column(
            "prevention_id",
            sa.Integer(),
            sa.ForeignKey("incident_prevention.ip_id"),
            nullable=True,
        ),

        sa.Column("sl_no", sa.Integer(), nullable=True),
        sa.Column("member_name", sa.String(length=150), nullable=True),
        sa.Column("designation", sa.String(length=150), nullable=True),
        sa.Column("station", sa.String(length=150), nullable=True),
        sa.Column("role", sa.String(length=50), nullable=True),

        sa.Column("created_by", sa.String(length=100), nullable=True),
        sa.Column("updated_by", sa.String(length=100), nullable=True),

        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.func.now(),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=True,
        ),
    )

    # --------------------------------------------
    # incident_investigation_team_history
    # --------------------------------------------
    op.create_table(
        "incident_investigation_team_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),

        sa.Column("iit_id", sa.Integer(), nullable=True),
        sa.Column("prevention_id", sa.Integer(), nullable=True),

        sa.Column("sl_no", sa.Integer(), nullable=True),
        sa.Column("member_name", sa.String(length=150), nullable=True),
        sa.Column("designation", sa.String(length=150), nullable=True),
        sa.Column("station", sa.String(length=150), nullable=True),
        sa.Column("role", sa.String(length=50), nullable=True),

        sa.Column("created_by", sa.String(length=100), nullable=True),
        sa.Column("updated_by", sa.String(length=100), nullable=True),

        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.func.now(),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=True,
        ),
    )


def downgrade():
    op.drop_table("incident_investigation_team_history")
    op.drop_table("incident_investigation_team")