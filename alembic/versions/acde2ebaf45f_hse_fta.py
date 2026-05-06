"""hse fta

Revision ID: acde2ebaf45f
Revises: 7d37336a7bda
Create Date: 2026-02-03 17:21:25.640492

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'acde2ebaf45f'
down_revision: Union[str, Sequence[str], None] = '7d37336a7bda'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # 1️⃣ Rename incident_id → hiim_id
    op.alter_column(
        "hse_incident_rca_5why",
        "incident_id",
        new_column_name="hiim_id"
    )

    op.alter_column(
        "hse_incident_rca_5why_history",
        "incident_id",
        new_column_name="hiim_id"
    )

    # 2️⃣ Add hiim_id as NULLABLE first
    op.add_column(
        "fta_top_event",
        sa.Column("hiim_id", sa.Integer(), nullable=True)
    )

    op.add_column(
        "fta_top_event_history",
        sa.Column("hiim_id", sa.Integer(), nullable=True)
    )

    # 3️⃣ Backfill hiim_id (IMPORTANT)
    # ⚠️ Adjust logic if mapping is different
    op.execute("""
        UPDATE fta_top_event
        SET hiim_id = (
            SELECT hiim_id
            FROM hse_incident_investigation_master
            LIMIT 1
        )
    """)

    op.execute("""
        UPDATE fta_top_event_history
        SET hiim_id = (
            SELECT hiim_id
            FROM hse_incident_investigation_master
            LIMIT 1
        )
    """)

    # 4️⃣ Set NOT NULL
    op.alter_column(
        "fta_top_event",
        "hiim_id",
        nullable=False
    )

    op.alter_column(
        "fta_top_event_history",
        "hiim_id",
        nullable=False
    )

    # 5️⃣ Add foreign keys
    op.create_foreign_key(
        "fk_fta_top_event_hiim_id",
        "fta_top_event",
        "hse_incident_investigation_master",
        ["hiim_id"],
        ["hiim_id"],
        ondelete="CASCADE"
    )

    op.create_foreign_key(
        "fk_fta_top_event_history_hiim_id",
        "fta_top_event_history",
        "hse_incident_investigation_master",
        ["hiim_id"],
        ["hiim_id"],
        ondelete="CASCADE"
    )
def downgrade():
    op.drop_constraint(
        "fk_fta_top_event_hiim_id",
        "fta_top_event",
        type_="foreignkey"
    )
    op.drop_constraint(
        "fk_fta_top_event_history_hiim_id",
        "fta_top_event_history",
        type_="foreignkey"
    )

    op.drop_column("fta_top_event", "hiim_id")
    op.drop_column("fta_top_event_history", "hiim_id")

    op.alter_column(
        "hse_incident_rca_5why",
        "hiim_id",
        new_column_name="incident_id"
    )

    op.alter_column(
        "hse_incident_rca_5why_history",
        "hiim_id",
        new_column_name="incident_id"
    )