"""move role and ack fields to incident investigation team tables

Revision ID: ac7713255bcb
Revises: c8bf6ce5bedd
Create Date: 2026-02-16 12:55:56.245255

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ac7713255bcb'
down_revision: Union[str, Sequence[str], None] = 'c8bf6ce5bedd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():

    # =====================================================
    # ADD to incident_investigation_team
    # =====================================================
    op.add_column(
        "incident_investigation_team",
        sa.Column("is_leader", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column(
        "incident_investigation_team",
        sa.Column("is_member", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.add_column(
        "incident_investigation_team",
        sa.Column("leader_acknowledged", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column(
        "incident_investigation_team",
        sa.Column("leader_acknowledged_at", sa.DateTime(), nullable=True),
    )
    op.add_column(
        "incident_investigation_team",
        sa.Column("member_acknowledged", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column(
        "incident_investigation_team",
        sa.Column("member_acknowledged_at", sa.DateTime(), nullable=True),
    )

    # =====================================================
    # ADD to incident_investigation_team_history
    # =====================================================
    op.add_column(
        "incident_investigation_team_history",
        sa.Column("is_leader", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column(
        "incident_investigation_team_history",
        sa.Column("is_member", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.add_column(
        "incident_investigation_team_history",
        sa.Column("leader_acknowledged", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column(
        "incident_investigation_team_history",
        sa.Column("leader_acknowledged_at", sa.DateTime(), nullable=True),
    )
    op.add_column(
        "incident_investigation_team_history",
        sa.Column("member_acknowledged", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column(
        "incident_investigation_team_history",
        sa.Column("member_acknowledged_at", sa.DateTime(), nullable=True),
    )

    # =====================================================
    # REMOVE from OLD hse tables
    # =====================================================
    op.drop_column("hse_incident_investigation_team", "member_acknowledged_at")
    op.drop_column("hse_incident_investigation_team", "member_acknowledged")
    op.drop_column("hse_incident_investigation_team", "leader_acknowledged_at")
    op.drop_column("hse_incident_investigation_team", "leader_acknowledged")
    op.drop_column("hse_incident_investigation_team", "is_member")
    op.drop_column("hse_incident_investigation_team", "is_leader")

    op.drop_column("hse_incident_investigation_team_history", "member_acknowledged_at")
    op.drop_column("hse_incident_investigation_team_history", "member_acknowledged")
    op.drop_column("hse_incident_investigation_team_history", "leader_acknowledged_at")
    op.drop_column("hse_incident_investigation_team_history", "leader_acknowledged")
    op.drop_column("hse_incident_investigation_team_history", "is_member")
    op.drop_column("hse_incident_investigation_team_history", "is_leader")


def downgrade():

    # =====================================================
    # ADD back to old hse tables
    # =====================================================
    op.add_column("hse_incident_investigation_team",
        sa.Column("is_leader", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column("hse_incident_investigation_team",
        sa.Column("is_member", sa.Boolean(), nullable=False, server_default=sa.true()))
    op.add_column("hse_incident_investigation_team",
        sa.Column("leader_acknowledged", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column("hse_incident_investigation_team",
        sa.Column("leader_acknowledged_at", sa.DateTime(), nullable=True))
    op.add_column("hse_incident_investigation_team",
        sa.Column("member_acknowledged", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column("hse_incident_investigation_team",
        sa.Column("member_acknowledged_at", sa.DateTime(), nullable=True))

    op.add_column("hse_incident_investigation_team_history",
        sa.Column("is_leader", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column("hse_incident_investigation_team_history",
        sa.Column("is_member", sa.Boolean(), nullable=False, server_default=sa.true()))
    op.add_column("hse_incident_investigation_team_history",
        sa.Column("leader_acknowledged", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column("hse_incident_investigation_team_history",
        sa.Column("leader_acknowledged_at", sa.DateTime(), nullable=True))
    op.add_column("hse_incident_investigation_team_history",
        sa.Column("member_acknowledged", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column("hse_incident_investigation_team_history",
        sa.Column("member_acknowledged_at", sa.DateTime(), nullable=True))

    # =====================================================
    # REMOVE from new incident tables
    # =====================================================
    op.drop_column("incident_investigation_team_history", "member_acknowledged_at")
    op.drop_column("incident_investigation_team_history", "member_acknowledged")
    op.drop_column("incident_investigation_team_history", "leader_acknowledged_at")
    op.drop_column("incident_investigation_team_history", "leader_acknowledged")
    op.drop_column("incident_investigation_team_history", "is_member")
    op.drop_column("incident_investigation_team_history", "is_leader")

    op.drop_column("incident_investigation_team", "member_acknowledged_at")
    op.drop_column("incident_investigation_team", "member_acknowledged")
    op.drop_column("incident_investigation_team", "leader_acknowledged_at")
    op.drop_column("incident_investigation_team", "leader_acknowledged")
    op.drop_column("incident_investigation_team", "is_member")
    op.drop_column("incident_investigation_team", "is_leader")