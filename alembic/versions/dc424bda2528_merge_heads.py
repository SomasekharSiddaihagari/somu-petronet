"""merge heads

Revision ID: dc424bda2528
Revises: 4b3dad94f8fa, 73c0ea35d73e
Create Date: 2025-11-27 11:04:48.011593

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc424bda2528'
down_revision: Union[str, Sequence[str], None] = ('4b3dad94f8fa', '73c0ea35d73e')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
