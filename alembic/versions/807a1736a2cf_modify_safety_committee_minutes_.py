"""modify safety committee minutes structure

Revision ID: 807a1736a2cf
Revises: 6d846fa79e12
Create Date: 2026-02-24 20:24:16.599176

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '807a1736a2cf'
down_revision: Union[str, Sequence[str], None] = '6d846fa79e12'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    # =====================================================
    # SAFETY COMMITTEE MINUTES TABLE
    # =====================================================

    # meeting_no: increase size + make not null
    op.alter_column(
        "safety_committee_minutes",
        "meeting_no",
        existing_type=sa.String(length=50),
        type_=sa.String(length=100),
        nullable=False,
    )

    # location size change
    op.alter_column(
        "safety_committee_minutes",
        "location",
        existing_type=sa.String(length=150),
        type_=sa.String(length=255),
        nullable=True,
    )

    # frequency size change
    op.alter_column(
        "safety_committee_minutes",
        "frequency",
        existing_type=sa.String(length=50),
        type_=sa.String(length=100),
        nullable=True,
    )

    # 🔥 KEEP next_meeting as STRING (NO DATE CONVERSION)

    # Drop old unused columns
    op.drop_column("safety_committee_minutes", "description_of_discussion")
    op.drop_column("safety_committee_minutes", "issues_discussed")
    op.drop_column("safety_committee_minutes", "action_taken")
    op.drop_column("safety_committee_minutes", "completed_on")
    op.drop_column("safety_committee_minutes", "action_by")
    op.drop_column("safety_committee_minutes", "target_date")
    op.drop_column("safety_committee_minutes", "incident_id")
    op.drop_column("safety_committee_minutes", "is_active")

    # Add unique constraint
    op.create_unique_constraint(
        "uq_scmm_meeting_no",
        "safety_committee_minutes",
        ["meeting_no"],
    )

    # =====================================================
    # HISTORY TABLE
    # =====================================================

    # Rename scmm_id → scm_id
    op.alter_column(
        "safety_committee_minutes_history",
        "scmm_id",
        new_column_name="scm_id",
    )

    # meeting_no size change
    op.alter_column(
        "safety_committee_minutes_history",
        "meeting_no",
        existing_type=sa.String(length=50),
        type_=sa.String(length=100),
        nullable=False,
    )

    # location size change
    op.alter_column(
        "safety_committee_minutes_history",
        "location",
        existing_type=sa.String(length=150),
        type_=sa.String(length=255),
    )

    # frequency size change
    op.alter_column(
        "safety_committee_minutes_history",
        "frequency",
        existing_type=sa.String(length=50),
        type_=sa.String(length=100),
    )

    # Drop old unused columns
    op.drop_column("safety_committee_minutes_history", "description_of_discussion")
    op.drop_column("safety_committee_minutes_history", "issues_discussed")
    op.drop_column("safety_committee_minutes_history", "action_taken")
    op.drop_column("safety_committee_minutes_history", "completed_on")
    op.drop_column("safety_committee_minutes_history", "action_by")
    op.drop_column("safety_committee_minutes_history", "target_date")
    op.drop_column("safety_committee_minutes_history", "incident_id")
    op.drop_column("safety_committee_minutes_history", "is_active")

    # Add unique constraint
    op.create_unique_constraint(
        "uq_scmm_meeting_no_history",
        "safety_committee_minutes_history",
        ["meeting_no"],
    )


def downgrade():

    # =====================================================
    # SAFETY COMMITTEE MINUTES TABLE
    # =====================================================

    op.drop_constraint("uq_scmm_meeting_no", "safety_committee_minutes", type_="unique")

    op.add_column("safety_committee_minutes", sa.Column("description_of_discussion", sa.Text(), nullable=True))
    op.add_column("safety_committee_minutes", sa.Column("issues_discussed", sa.Text(), nullable=True))
    op.add_column("safety_committee_minutes", sa.Column("action_taken", sa.Text(), nullable=True))
    op.add_column("safety_committee_minutes", sa.Column("completed_on", sa.Date(), nullable=True))
    op.add_column("safety_committee_minutes", sa.Column("action_by", sa.String(length=150), nullable=True))
    op.add_column("safety_committee_minutes", sa.Column("target_date", sa.Date(), nullable=True))
    op.add_column("safety_committee_minutes", sa.Column("incident_id", sa.Integer(), nullable=True))
    op.add_column("safety_committee_minutes", sa.Column("is_active", sa.Boolean(), nullable=True))

    # revert column sizes
    op.alter_column(
        "safety_committee_minutes",
        "meeting_no",
        existing_type=sa.String(length=100),
        type_=sa.String(length=50),
        nullable=True,
    )

    op.alter_column(
        "safety_committee_minutes",
        "location",
        existing_type=sa.String(length=255),
        type_=sa.String(length=150),
    )

    op.alter_column(
        "safety_committee_minutes",
        "frequency",
        existing_type=sa.String(length=100),
        type_=sa.String(length=50),
    )

    # =====================================================
    # HISTORY TABLE
    # =====================================================

    op.drop_constraint("uq_scmm_meeting_no_history", "safety_committee_minutes_history", type_="unique")

    op.add_column("safety_committee_minutes_history", sa.Column("description_of_discussion", sa.Text(), nullable=True))
    op.add_column("safety_committee_minutes_history", sa.Column("issues_discussed", sa.Text(), nullable=True))
    op.add_column("safety_committee_minutes_history", sa.Column("action_taken", sa.Text(), nullable=True))
    op.add_column("safety_committee_minutes_history", sa.Column("completed_on", sa.Date(), nullable=True))
    op.add_column("safety_committee_minutes_history", sa.Column("action_by", sa.String(length=150), nullable=True))
    op.add_column("safety_committee_minutes_history", sa.Column("target_date", sa.Date(), nullable=True))
    op.add_column("safety_committee_minutes_history", sa.Column("incident_id", sa.Integer(), nullable=True))
    op.add_column("safety_committee_minutes_history", sa.Column("is_active", sa.Boolean(), nullable=True))

    # revert rename
    op.alter_column(
        "safety_committee_minutes_history",
        "scm_id",
        new_column_name="scmm_id",
    )

    # revert column sizes
    op.alter_column(
        "safety_committee_minutes_history",
        "meeting_no",
        existing_type=sa.String(length=100),
        type_=sa.String(length=50),
        nullable=True,
    )

    op.alter_column(
        "safety_committee_minutes_history",
        "location",
        existing_type=sa.String(length=255),
        type_=sa.String(length=150),
    )

    op.alter_column(
        "safety_committee_minutes_history",
        "frequency",
        existing_type=sa.String(length=100),
        type_=sa.String(length=50),
    )