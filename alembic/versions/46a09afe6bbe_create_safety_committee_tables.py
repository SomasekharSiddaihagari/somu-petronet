"""create safety committee tables

Revision ID: 46a09afe6bbe
Revises: 0e415ce65f87
Create Date: 2026-02-04 12:38:24.070528

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '46a09afe6bbe'
down_revision: Union[str, Sequence[str], None] = '0e415ce65f87'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():

    # ------------------------------------------------------------------
    # safety_committee_members
    # ------------------------------------------------------------------
    op.create_table(
        "safety_committee_members",
        sa.Column("scm_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("meeting_id", sa.Integer, nullable=True),
        sa.Column("name", sa.String(100), nullable=True),
        sa.Column("designation", sa.String(100), nullable=True),
        sa.Column("station", sa.Integer, nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=True),
        sa.Column("created_by", sa.Integer, nullable=True),
        sa.Column("updated_by", sa.Integer, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
    )

    # ------------------------------------------------------------------
    # safety_committee_members_history
    # ------------------------------------------------------------------
    op.create_table(
        "safety_committee_members_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("scm_id", sa.Integer, nullable=True),
        sa.Column("meeting_id", sa.Integer, nullable=True),
        sa.Column("name", sa.String(100), nullable=True),
        sa.Column("designation", sa.String(100), nullable=True),
        sa.Column("station", sa.Integer, nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=True),
        sa.Column("created_by", sa.Integer, nullable=True),
        sa.Column("updated_by", sa.Integer, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
    )

    # ------------------------------------------------------------------
    # safety_committee_quarterly_meetings
    # ------------------------------------------------------------------
    op.create_table(
        "safety_committee_quarterly_meetings",
        sa.Column("scm_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("location", sa.String(150), nullable=True),
        sa.Column("meeting_date", sa.Date, nullable=True),
        sa.Column("meeting_time", sa.Time, nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=True),
        sa.Column("created_by", sa.Integer, nullable=True),
        sa.Column("updated_by", sa.Integer, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
    )

    # ------------------------------------------------------------------
    # safety_committee_meetings_quarterly_history
    # ------------------------------------------------------------------
    op.create_table(
        "safety_committee_meetings_quarterly_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("scm_id", sa.Integer, nullable=True),
        sa.Column("location", sa.String(150), nullable=True),
        sa.Column("meeting_date", sa.Date, nullable=True),
        sa.Column("meeting_time", sa.Time, nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=True),
        sa.Column("created_by", sa.Integer, nullable=True),
        sa.Column("updated_by", sa.Integer, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
    )

    # ------------------------------------------------------------------
    # safety_committee_minutes
    # ------------------------------------------------------------------
    op.create_table(
        "safety_committee_minutes",
        sa.Column("scmm_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("meeting_no", sa.String(50), nullable=True),
        sa.Column("location", sa.String(150), nullable=True),
        sa.Column("frequency", sa.String(50), nullable=True),
        sa.Column("meeting_date", sa.Date, nullable=True),
        sa.Column("description_of_discussion", sa.Text, nullable=True),
        sa.Column("issues_discussed", sa.Text, nullable=True),
        sa.Column("action_taken", sa.Text, nullable=True),
        sa.Column("completed_on", sa.Date, nullable=True),
        sa.Column("action_by", sa.String(150), nullable=True),
        sa.Column("target_date", sa.Date, nullable=True),
        sa.Column("incident_id", sa.Integer, nullable=True),
        sa.Column("next_meeting", sa.String(100), nullable=True),
        sa.Column("created_by", sa.Integer, nullable=True),
        sa.Column("updated_by", sa.Integer, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
    )

    # ------------------------------------------------------------------
    # safety_committee_minutes_history
    # ------------------------------------------------------------------
    op.create_table(
        "safety_committee_minutes_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("scmm_id", sa.Integer, nullable=True),
        sa.Column("meeting_no", sa.String(50), nullable=True),
        sa.Column("location", sa.String(150), nullable=True),
        sa.Column("frequency", sa.String(50), nullable=True),
        sa.Column("meeting_date", sa.Date, nullable=True),
        sa.Column("description_of_discussion", sa.Text, nullable=True),
        sa.Column("issues_discussed", sa.Text, nullable=True),
        sa.Column("action_taken", sa.Text, nullable=True),
        sa.Column("completed_on", sa.Date, nullable=True),
        sa.Column("action_by", sa.String(150), nullable=True),
        sa.Column("target_date", sa.Date, nullable=True),
        sa.Column("incident_id", sa.Integer, nullable=True),
        sa.Column("next_meeting", sa.String(100), nullable=True),
        sa.Column("created_by", sa.Integer, nullable=True),
        sa.Column("updated_by", sa.Integer, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
    )

    # ------------------------------------------------------------------
    # safety_committee_minutes_members
    # ------------------------------------------------------------------
    op.create_table(
        "safety_committee_minutes_members",
        sa.Column("scmm_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column(
            "minutes_id",
            sa.Integer,
            sa.ForeignKey("safety_committee_minutes.scmm_id"),
            nullable=True,
        ),
        sa.Column("member_name", sa.String(150), nullable=True),
        sa.Column("created_by", sa.Integer, nullable=True),
        sa.Column("updated_by", sa.Integer, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
    )

    # ------------------------------------------------------------------
    # safety_committee_minutes_members_history
    # ------------------------------------------------------------------
    op.create_table(
        "safety_committee_minutes_members_history",
        sa.Column("history_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("scmm_id", sa.Integer, nullable=True),
        sa.Column(
            "minutes_id",
            sa.Integer,
            sa.ForeignKey("safety_committee_minutes.scmm_id"),
            nullable=True,
        ),
        sa.Column("member_name", sa.String(150), nullable=True),
        sa.Column("created_by", sa.Integer, nullable=True),
        sa.Column("updated_by", sa.Integer, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
    )
def downgrade():
    op.drop_table("safety_committee_minutes_members_history")
    op.drop_table("safety_committee_minutes_members")
    op.drop_table("safety_committee_minutes_history")
    op.drop_table("safety_committee_minutes")
    op.drop_table("safety_committee_meetings_quarterly_history")
    op.drop_table("safety_committee_quarterly_meetings")
    op.drop_table("safety_committee_members_history")
    op.drop_table("safety_committee_members")