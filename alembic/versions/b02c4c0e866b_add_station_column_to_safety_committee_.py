"""add station column to safety committee minutes

Revision ID: b02c4c0e866b
Revises: 2a168218e820
Create Date: 2026-02-26 14:56:53.845082

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b02c4c0e866b'
down_revision: Union[str, Sequence[str], None] = '2a168218e820'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
