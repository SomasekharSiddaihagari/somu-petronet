"""add role and ack columns to hse incident investigation team

Revision ID: b9a585256e72
Revises: e9ddb9444e89
Create Date: 2026-02-16 12:33:23.280558

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b9a585256e72'
down_revision: Union[str, Sequence[str], None] = 'e9ddb9444e89'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # ================================
    # hse_incident_investigation_team
    # ================================
    op.add_column(
        "hse_incident_investigation_team",
        sa.Column("is_leader", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column(
        "hse_incident_investigation_team",
        sa.Column("is_member", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.add_column(
        "hse_incident_investigation_team",
        sa.Column("leader_acknowledged", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column(
        "hse_incident_investigation_team",
        sa.Column("leader_acknowledged_at", sa.DateTime(), nullable=True),
    )
    op.add_column(
        "hse_incident_investigation_team",
        sa.Column("member_acknowledged", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column(
        "hse_incident_investigation_team",
        sa.Column("member_acknowledged_at", sa.DateTime(), nullable=True),
    )

    # =========================================
    # hse_incident_investigation_team_history
    # =========================================
    op.add_column(
        "hse_incident_investigation_team_history",
        sa.Column("is_leader", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column(
        "hse_incident_investigation_team_history",
        sa.Column("is_member", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.add_column(
        "hse_incident_investigation_team_history",
        sa.Column("leader_acknowledged", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column(
        "hse_incident_investigation_team_history",
        sa.Column("leader_acknowledged_at", sa.DateTime(), nullable=True),
    )
    op.add_column(
        "hse_incident_investigation_team_history",
        sa.Column("member_acknowledged", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column(
        "hse_incident_investigation_team_history",
        sa.Column("member_acknowledged_at", sa.DateTime(), nullable=True),
    )


def downgrade():
    # main table
    op.drop_column("hse_incident_investigation_team", "member_acknowledged_at")
    op.drop_column("hse_incident_investigation_team", "member_acknowledged")
    op.drop_column("hse_incident_investigation_team", "leader_acknowledged_at")
    op.drop_column("hse_incident_investigation_team", "leader_acknowledged")
    op.drop_column("hse_incident_investigation_team", "is_member")
    op.drop_column("hse_incident_investigation_team", "is_leader")

    # history table
    op.drop_column("hse_incident_investigation_team_history", "member_acknowledged_at")
    op.drop_column("hse_incident_investigation_team_history", "member_acknowledged")
    op.drop_column("hse_incident_investigation_team_history", "leader_acknowledged_at")
    op.drop_column("hse_incident_investigation_team_history", "leader_acknowledged")
    op.drop_column("hse_incident_investigation_team_history", "is_member")
    op.drop_column("hse_incident_investigation_team_history", "is_leader")