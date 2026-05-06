"""create circular attachments tables

Revision ID: a563598a2c05
Revises: 382f30047007
Create Date: 2026-02-05 18:50:55.913395

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a563598a2c05'
down_revision: Union[str, Sequence[str], None] = '382f30047007'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    # ===============================
    # circular_attachments
    # ===============================
    op.create_table(
        "circular_attachments",

        sa.Column("attachment_id", sa.Integer(), primary_key=True, autoincrement=True),

        sa.Column(
            "circular_id",
            sa.Integer(),
            sa.ForeignKey("circular_master.circular_id", ondelete="CASCADE"),
            nullable=False
        ),

        sa.Column("file_name", sa.String(), nullable=True),
        sa.Column("file_path", sa.String(), nullable=True),
        sa.Column("file_type", sa.String(), nullable=True),
        sa.Column("file_size", sa.BigInteger(), nullable=True),

        sa.Column(
            "uploaded_by",
            sa.Integer(),
            sa.ForeignKey("users.user_id"),
            nullable=False
        ),

        sa.Column(
            "uploaded_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now()
        )
    )

    # ===============================
    # circular_attachments_history
    # ===============================
    op.create_table(
        "circular_attachments_history",

        sa.Column("history_id", sa.Integer(), primary_key=True, autoincrement=True),

        sa.Column("attachment_id", sa.Integer(), nullable=True),

        sa.Column(
            "circular_id",
            sa.Integer(),
            sa.ForeignKey("circular_master.circular_id", ondelete="CASCADE"),
            nullable=False
        ),

        sa.Column("file_name", sa.String(), nullable=True),
        sa.Column("file_path", sa.String(), nullable=True),
        sa.Column("file_type", sa.String(), nullable=True),
        sa.Column("file_size", sa.BigInteger(), nullable=True),

        sa.Column(
            "uploaded_by",
            sa.Integer(),
            sa.ForeignKey("users.user_id"),
            nullable=False
        ),

        sa.Column(
            "uploaded_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now()
        )
    )


def downgrade():
    op.drop_table("circular_attachments_history")
    op.drop_table("circular_attachments")
