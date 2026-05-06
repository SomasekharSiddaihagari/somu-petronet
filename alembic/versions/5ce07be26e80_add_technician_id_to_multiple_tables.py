"""add technician_id to multiple tables

Revision ID: 5ce07be26e80
Revises: 85f7efe06dfd
Create Date: 2026-03-23 10:44:03.002793

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5ce07be26e80'
down_revision: Union[str, Sequence[str], None] = '85f7efe06dfd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
