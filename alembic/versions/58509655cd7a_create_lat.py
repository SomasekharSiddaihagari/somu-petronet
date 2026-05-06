"""change lat lon from float to string

Revision ID: 58509655cd7a
Revises: 362b40450aae
Create Date: 2026-01-22 20:10:09.361470
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '58509655cd7a'
down_revision: Union[str, Sequence[str], None] = '362b40450aae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Change lat from FLOAT to VARCHAR(45)
    op.alter_column(
        "access_control_station",
        "lat",
        type_=sa.String(45),
        existing_type=sa.Float(),
        nullable=True,
    )

    # Change lon from FLOAT to VARCHAR(45)
    op.alter_column(
        "access_control_station",
        "lon",
        type_=sa.String(45),
        existing_type=sa.Float(),
        nullable=True,
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Revert lat back to FLOAT
    op.alter_column(
        "access_control_station",
        "lat",
        type_=sa.Float(),
        existing_type=sa.String(45),
        nullable=True,
    )

    # Revert lon back to FLOAT
    op.alter_column(
        "access_control_station",
        "lon",
        type_=sa.Float(),
        existing_type=sa.String(45),
        nullable=True,
    )
