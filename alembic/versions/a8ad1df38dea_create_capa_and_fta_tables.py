"""create capa and fta tables

Revision ID: a8ad1df38dea
Revises: 5dc74e8279b8
Create Date: 2026-02-02 12:59:02.682071

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a8ad1df38dea'
down_revision: Union[str, Sequence[str], None] = '5dc74e8279b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    # =====================================================
    # CAPA ACTIONS
    # =====================================================
    op.create_table(
        "hse_incident_capa_actions",
        sa.Column("capa_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "incident_id",
            sa.Integer(),
            sa.ForeignKey(
                "hse_incident_investigation_master.hiim_id",
                ondelete="CASCADE"
            ),
            nullable=False,
        ),
        sa.Column("action", sa.Text(), nullable=True),
        sa.Column("action_type", sa.String(20), nullable=True),
        sa.Column("target_date", sa.Date(), nullable=True),
    )

    op.create_table(
        "hse_incident_capa_actions_history",
        sa.Column("historyid", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("capa_id", sa.Integer(), nullable=True),
        sa.Column("incident_id", sa.Integer(), nullable=True),
        sa.Column("action", sa.Text(), nullable=True),
        sa.Column("action_type", sa.String(20), nullable=True),
        sa.Column("target_date", sa.Date(), nullable=True),
    )

    # =====================================================
    # FTA – TOP EVENT
    # =====================================================
    op.create_table(
        "fta_top_event",
        sa.Column("fta_top_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("event_description", sa.String(500), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.func.now()
        ),
    )

    op.create_table(
        "fta_top_event_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("fta_top_id", sa.Integer(), nullable=True),
        sa.Column("event_description", sa.String(500), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.func.now()
        ),
    )

    # =====================================================
    # FTA – INTERMEDIATE EVENT
    # =====================================================
    op.create_table(
        "fta_intermediate_event",
        sa.Column(
            "intermediate_event_id",
            sa.Integer(),
            primary_key=True,
            autoincrement=True
        ),
        sa.Column(
            "top_event_id",
            sa.Integer(),
            sa.ForeignKey("fta_top_event.fta_top_id"),
            nullable=False,
        ),
        sa.Column("intermediate_e1", sa.String(500), nullable=True),
        sa.Column("intermediate_e2", sa.String(500), nullable=True),
    )

    op.create_table(
        "fta_intermediate_event_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("intermediate_event_id", sa.Integer(), nullable=True),
        sa.Column(
            "top_event_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column("intermediate_e1", sa.String(500), nullable=True),
        sa.Column("intermediate_e2", sa.String(500), nullable=True),
    )

    # =====================================================
    # FTA – BASIC EVENT
    # =====================================================
    op.create_table(
        "fta_basic_event",
        sa.Column("fte_basic_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "intermediate_event_id",
            sa.Integer(),
            sa.ForeignKey(
                "fta_intermediate_event.intermediate_event_id"
            ),
            nullable=False,
        ),
        sa.Column("e1_b1", sa.String(500), nullable=True),
        sa.Column("e1_b2", sa.String(500), nullable=True),
        sa.Column("e2_b1", sa.String(500), nullable=True),
        sa.Column("e2_b2", sa.String(500), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.func.now()
        ),
    )

    op.create_table(
        "fta_basic_event_history",
        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("fte_basic_id", sa.Integer(), nullable=True),
        sa.Column("intermediate_event_id", sa.Integer(), nullable=False),
        sa.Column("e1_b1", sa.String(500), nullable=True),
        sa.Column("e1_b2", sa.String(500), nullable=True),
        sa.Column("e2_b1", sa.String(500), nullable=True),
        sa.Column("e2_b2", sa.String(500), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.func.now()
        ),
    )


def downgrade():
    op.drop_table("fta_basic_event_history")
    op.drop_table("fta_basic_event")
    op.drop_table("fta_intermediate_event_history")
    op.drop_table("fta_intermediate_event")
    op.drop_table("fta_top_event_history")
    op.drop_table("fta_top_event")
    op.drop_table("hse_incident_capa_actions_history")
    op.drop_table("hse_incident_capa_actions")