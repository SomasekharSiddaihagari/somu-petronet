"""add technician_id to npt logbook tables

Revision ID: 6a24c8c68675
Revises: f2bdb6429034
Create Date: 2026-03-16 11:57:08.244438

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a24c8c68675'
down_revision: Union[str, Sequence[str], None] = 'f2bdb6429034'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
