"""change shutdown_required to boolean in moc tables

Revision ID: 895ec1834212
Revises: c28dd2adc704
Create Date: 2026-01-12 12:32:59.313019

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '895ec1834212'
down_revision: Union[str, Sequence[str], None] = 'c28dd2adc704'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ---- moc_requests ----
    op.alter_column(
        "moc_requests",
        "shutdown_required",
        existing_type=sa.String(length=20),
        type_=sa.Boolean(),
        existing_nullable=True,
        postgresql_using="""
            CASE
                WHEN LOWER(shutdown_required) IN ('yes', 'true', '1') THEN true
                ELSE false
            END
        """
    )

    # ---- moc_request_history ----
    op.alter_column(
        "moc_request_history",
        "shutdown_required",
        existing_type=sa.String(length=20),
        type_=sa.Boolean(),
        existing_nullable=True,
        postgresql_using="""
            CASE
                WHEN LOWER(shutdown_required) IN ('yes', 'true', '1') THEN true
                ELSE false
            END
        """
    )


def downgrade():
    # ---- moc_requests ----
    op.alter_column(
        "moc_requests",
        "shutdown_required",
        existing_type=sa.Boolean(),
        type_=sa.String(length=20),
        existing_nullable=True,
        postgresql_using="""
            CASE
                WHEN shutdown_required = true THEN 'Yes'
                ELSE 'No'
            END
        """
    )

    # ---- moc_request_history ----
    op.alter_column(
        "moc_request_history",
        "shutdown_required",
        existing_type=sa.Boolean(),
        type_=sa.String(length=20),
        existing_nullable=True,
        postgresql_using="""
            CASE
                WHEN shutdown_required = true THEN 'Yes'
                ELSE 'No'
            END
        """
    )