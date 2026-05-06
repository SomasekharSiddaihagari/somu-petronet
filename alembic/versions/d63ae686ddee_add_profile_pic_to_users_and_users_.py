"""add profile_pic to users and users_history

Revision ID: d63ae686ddee
Revises: 0251237b2f46
Create Date: 2026-01-05 12:32:35.065160

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd63ae686ddee'
down_revision: Union[str, Sequence[str], None] = '0251237b2f46'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "users",
        sa.Column("profile_pic", sa.Text(), nullable=True)
    )

    op.add_column(
        "users_history",
        sa.Column("profile_pic", sa.Text(), nullable=True)
    )


def downgrade():
    op.drop_column("users_history", "profile_pic")
    op.drop_column("users", "profile_pic")