"""tables of change of claim submissions

Revision ID: 1b6f6238ae96
Revises: bb77b17d42cf
Create Date: 2025-12-26 16:27:35.728935

"""
from typing import Sequence, Union
from sqlalchemy.engine.reflection import Inspector
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b6f6238ae96'
down_revision: Union[str, Sequence[str], None] = 'bb77b17d42cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def column_exists(inspector: Inspector, table: str, column: str) -> bool:
    return column in [c["name"] for c in inspector.get_columns(table)]


def upgrade():
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)

    # -------------------------------
    # REQUIRED COLUMNS
    # -------------------------------
    columns = {
        "residual_value_percent": sa.Numeric(5, 2),
        "residual_value_amount": sa.Numeric(12, 2),
        "amount_to_be_disbursed": sa.Numeric(12, 2),
        "hr_comment": sa.Text(),
        "finance_comment": sa.Text(),
        "supervisor_comment": sa.Text(),
    }

    # -------------------------------
    # ADD TO asset_claim_submission
    # -------------------------------
    for col, col_type in columns.items():
        if not column_exists(inspector, "asset_claim_submission", col):
            op.add_column(
                "asset_claim_submission",
                sa.Column(col, col_type, nullable=True),
            )

    # -------------------------------
    # ADD TO asset_claim_submission_history
    # -------------------------------
    for col, col_type in columns.items():
        if not column_exists(inspector, "asset_claim_submission_history", col):
            op.add_column(
                "asset_claim_submission_history",
                sa.Column(col, col_type, nullable=True),
            )

    # -------------------------------
    # REMOVE FROM asset_claim (WRONG TABLE)
    # -------------------------------
    for col in columns.keys():
        if column_exists(inspector, "asset_claim", col):
            op.drop_column("asset_claim", col)

    # -------------------------------
    # REMOVE FROM asset_claim_history (WRONG TABLE)
    # -------------------------------
    for col in columns.keys():
        if column_exists(inspector, "asset_claim_history", col):
            op.drop_column("asset_claim_history", col)


def downgrade():
    # ⚠️ Intentionally left empty
    # This migration is a corrective schema fix.
    pass