"""create moc request boolean

Revision ID: 4da73fd1a740
Revises: 7c36572b8e25
Create Date: 2026-01-22 10:53:59.037679

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4da73fd1a740'
down_revision: Union[str, Sequence[str], None] = '7c36572b8e25'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ---- moc_requests ----
    op.execute("""
        ALTER TABLE moc_requests
        ALTER COLUMN statutory_approval_required
        TYPE BOOLEAN
        USING (
            CASE
                WHEN LOWER(statutory_approval_required) = 'yes' THEN TRUE
                WHEN LOWER(statutory_approval_required) = 'no' THEN FALSE
                ELSE NULL
            END
        )
    """)

    # ---- moc_request_history ----
    op.execute("""
        ALTER TABLE moc_request_history
        ALTER COLUMN statutory_approval_required
        TYPE BOOLEAN
        USING (
            CASE
                WHEN LOWER(statutory_approval_required) = 'yes' THEN TRUE
                WHEN LOWER(statutory_approval_required) = 'no' THEN FALSE
                ELSE NULL
            END
        )
    """)


def downgrade():
    # ---- moc_requests ----
    op.execute("""
        ALTER TABLE moc_requests
        ALTER COLUMN statutory_approval_required
        TYPE VARCHAR(40)
        USING (
            CASE
                WHEN statutory_approval_required = TRUE THEN 'Yes'
                WHEN statutory_approval_required = FALSE THEN 'No'
                ELSE NULL
            END
        )
    """)

    # ---- moc_request_history ----
    op.execute("""
        ALTER TABLE moc_request_history
        ALTER COLUMN statutory_approval_required
        TYPE VARCHAR(40)
        USING (
            CASE
                WHEN statutory_approval_required = TRUE THEN 'Yes'
                WHEN statutory_approval_required = FALSE THEN 'No'
                ELSE NULL
            END
        )
    """)