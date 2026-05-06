"""Manually update roles table

Revision ID: 81cfbb20e3b7
Revises: 5c8631cdb60c
Create Date: 2025-10-28 14:07:54.141336

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '81cfbb20e3b7'
down_revision: Union[str, Sequence[str], None] = '5c8631cdb60c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
