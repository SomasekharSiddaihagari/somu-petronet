"""add submission_id to user_education tables

Revision ID: ead4f6361b87
Revises: 829d94e66ad8
Create Date: 2026-02-17 15:15:54.727871

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ead4f6361b87'
down_revision: Union[str, Sequence[str], None] = '829d94e66ad8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    # ==============================
    # user_education table
    # ==============================
    op.add_column(
        "user_education",
        sa.Column("submission_id", sa.Integer(), nullable=True)
    )

    op.create_foreign_key(
        "fk_user_education_submission",
        "user_education",
        "submission",
        ["submission_id"],
        ["submission_id"],
        ondelete="SET NULL"
    )

    # ==============================
    # user_education_history table
    # ==============================
    op.add_column(
        "user_education_history",
        sa.Column("submission_id", sa.Integer(), nullable=True)
    )


def downgrade():

    # history remove
    op.drop_column("user_education_history", "submission_id")

    # main table remove FK + column
    op.drop_constraint(
        "fk_user_education_submission",
        "user_education",
        type_="foreignkey"
    )

    op.drop_column("user_education", "submission_id")
