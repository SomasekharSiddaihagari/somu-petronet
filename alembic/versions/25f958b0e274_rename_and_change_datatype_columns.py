"""rename and change datatype columns

Revision ID: 25f958b0e274
Revises: d73d7ad56fe9
Create Date: 2026-02-18
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '25f958b0e274'
down_revision: Union[str, Sequence[str], None] = 'd73d7ad56fe9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    # 🔁 RENAME COLUMN users
    op.alter_column(
        'users',
        'cr_address_comment',
        new_column_name='cr_address_document_details'
    )

    op.alter_column(
        'users_history',
        'cr_address_comment',
        new_column_name='cr_address_document_details'
    )

    # 🧹 STEP 1: remove old string values (important)
    op.execute("""
        UPDATE hse_incident_investigation_master
        SET allotted_to_name = NULL
    """)

    op.execute("""
        UPDATE hse_incident_investigation_master_history
        SET allotted_to_name = NULL
    """)

    # 🔁 STEP 2: change datatype STRING → INTEGER
    op.alter_column(
        'hse_incident_investigation_master',
        'allotted_to_name',
        existing_type=sa.String(length=150),
        type_=sa.Integer(),
        postgresql_using='allotted_to_name::integer'
    )

    op.alter_column(
        'hse_incident_investigation_master_history',
        'allotted_to_name',
        existing_type=sa.String(length=150),
        type_=sa.Integer(),
        postgresql_using='allotted_to_name::integer'
    )


def downgrade():

    # revert rename
    op.alter_column(
        'users',
        'cr_address_document_details',
        new_column_name='cr_address_comment'
    )

    op.alter_column(
        'users_history',
        'cr_address_document_details',
        new_column_name='cr_address_comment'
    )

    # revert datatype INT → STRING
    op.alter_column(
        'hse_incident_investigation_master',
        'allotted_to_name',
        existing_type=sa.Integer(),
        type_=sa.String(length=150)
    )

    op.alter_column(
        'hse_incident_investigation_master_history',
        'allotted_to_name',
        existing_type=sa.Integer(),
        type_=sa.String(length=150)
    )
