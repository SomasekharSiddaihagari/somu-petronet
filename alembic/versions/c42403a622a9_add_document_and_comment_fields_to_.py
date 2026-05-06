"""add document and comment fields to users tables

Revision ID: c42403a622a9
Revises: ead4f6361b87
Create Date: 2026-02-17 15:48:41.736115

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c42403a622a9'
down_revision: Union[str, Sequence[str], None] = 'ead4f6361b87'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # USERS TABLE
    op.add_column("users", sa.Column("basic_document_details", sa.Text(), nullable=True))
    op.add_column("users", sa.Column("basic_comment", sa.Text(), nullable=True))

    op.add_column("users", sa.Column("address_document_details", sa.Text(), nullable=True))
    op.add_column("users", sa.Column("address_comment", sa.Text(), nullable=True))

    op.add_column("users", sa.Column("identity_document_details", sa.Text(), nullable=True))
    op.add_column("users", sa.Column("identity_comment", sa.Text(), nullable=True))

    # USERS HISTORY TABLE
    op.add_column("users_history", sa.Column("basic_document_details", sa.Text(), nullable=True))
    op.add_column("users_history", sa.Column("basic_comment", sa.Text(), nullable=True))

    op.add_column("users_history", sa.Column("address_document_details", sa.Text(), nullable=True))
    op.add_column("users_history", sa.Column("address_comment", sa.Text(), nullable=True))

    op.add_column("users_history", sa.Column("identity_document_details", sa.Text(), nullable=True))
    op.add_column("users_history", sa.Column("identity_comment", sa.Text(), nullable=True))


def downgrade():
    # USERS
    op.drop_column("users", "identity_comment")
    op.drop_column("users", "identity_document_details")
    op.drop_column("users", "address_comment")
    op.drop_column("users", "address_document_details")
    op.drop_column("users", "basic_comment")
    op.drop_column("users", "basic_document_details")

    # USERS HISTORY
    op.drop_column("users_history", "identity_comment")
    op.drop_column("users_history", "identity_document_details")
    op.drop_column("users_history", "address_comment")
    op.drop_column("users_history", "address_document_details")
    op.drop_column("users_history", "basic_comment")
    op.drop_column("users_history", "basic_document_details")