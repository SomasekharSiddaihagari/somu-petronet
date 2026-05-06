"""add document_name to employee_bank tables

Revision ID: 67f51fdc4b02
Revises: 6ab26a548b9d
Create Date: 2026-02-13 20:39:24.686583

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67f51fdc4b02'
down_revision: Union[str, Sequence[str], None] = '6ab26a548b9d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "employee_bank",
        sa.Column("document_name", sa.String(), nullable=True)
    )

    op.add_column(
        "employee_bank_history",
        sa.Column("document_name", sa.String(), nullable=True)
    )


def downgrade():
    op.drop_column("employee_bank", "document_name")
    op.drop_column("employee_bank_history", "document_name")