"""add user_id station_id to investigation team

Revision ID: 382f30047007
Revises: ce9ec48a3e05
Create Date: 2026-02-05 15:24:40.826061

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '382f30047007'
down_revision: Union[str, Sequence[str], None] = 'ce9ec48a3e05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():

    # ===============================
    # add columns to main table
    # ===============================
    op.add_column(
        "hse_incident_investigation_team",
        sa.Column("user_id", sa.Integer(), nullable=True)
    )

    op.add_column(
        "hse_incident_investigation_team",
        sa.Column("station_id", sa.Integer(), nullable=True)
    )

    # if incident_id FK needs change (optional)
    # drop old FK
    try:
        op.drop_constraint(
            "hse_incident_investigation_team_incident_id_fkey",
            "hse_incident_investigation_team",
            type_="foreignkey"
        )
    except:
        pass

    # add new FK to incident_report table
    op.create_foreign_key(
        "fk_investigation_incident",
        "hse_incident_investigation_team",
        "incident_report",
        ["incident_id"],
        ["incident_id"],
        ondelete="CASCADE"
    )

    # ===============================
    # HISTORY TABLE
    # ===============================
    op.add_column(
        "hse_incident_investigation_team_history",
        sa.Column("user_id", sa.Integer(), nullable=True)
    )

    op.add_column(
        "hse_incident_investigation_team_history",
        sa.Column("station_id", sa.Integer(), nullable=True)
    )


def downgrade():

    op.drop_column("hse_incident_investigation_team", "user_id")
    op.drop_column("hse_incident_investigation_team", "station_id")

    op.drop_column("hse_incident_investigation_team_history", "user_id")
    op.drop_column("hse_incident_investigation_team_history", "station_id")