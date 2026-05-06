"""Merge multiple heads

Revision ID: 541269591175
Revises: b3dda78de46d, f84e2d1a5d11
Create Date: 2025-10-31 15:55:06.279467

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '541269591175'
down_revision: Union[str, Sequence[str], None] = ('b3dda78de46d', 'f84e2d1a5d11')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
