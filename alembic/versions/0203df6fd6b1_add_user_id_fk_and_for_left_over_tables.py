"""add user_id FK and for left over tables

Revision ID: 0203df6fd6b1
Revises: 465b46b1bb5c
Create Date: 2025-12-10 12:57:17.850052

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0203df6fd6b1'
down_revision: Union[str, Sequence[str], None] = '465b46b1bb5c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    tables = [
        "travel_expense_sheet_detail",
        "travel_expense_sheet_detail_history",
        "daily_allowance_sheet_detail",
        "daily_allowance_sheet_detail_history"
    ]

    conn = op.get_bind()
    inspector = sa.inspect(conn)

    for table in tables:
        columns = [c['name'] for c in inspector.get_columns(table)]

        # Rename 'userid' to 'user_id' if exists
        if 'userid' in columns and 'user_id' not in columns:
            op.alter_column(table, 'userid', new_column_name='user_id')

        # Add 'user_id' if it does not exist
        if 'user_id' not in columns:
            op.add_column(table, sa.Column('user_id', sa.Integer(), nullable=True))

        # Create foreign key if not exists (skip if already exists)
        fk_name = f'fk_{table}_user_id'
        existing_fks = [fk['name'] for fk in inspector.get_foreign_keys(table)]
        if fk_name not in existing_fks:
            op.create_foreign_key(
                fk_name,
                table,
                'users',
                ['user_id'],
                ['user_id']
            )

    # Update emigration_required safely
    op.alter_column(
        'travel_requisition_history',
        'emigration_required',
        type_=sa.Boolean(),
        existing_type=sa.String(),
        existing_nullable=True,
        postgresql_using="emigration_required::boolean"
    )


def downgrade():
    tables = [
        "travel_expense_sheet_detail",
        "travel_expense_sheet_detail_history",
        "daily_allowance_sheet_detail",
        "daily_allowance_sheet_detail_history"
    ]

    conn = op.get_bind()
    inspector = sa.inspect(conn)

    for table in tables:
        columns = [c['name'] for c in inspector.get_columns(table)]
        existing_fks = [fk['name'] for fk in inspector.get_foreign_keys(table)]

        # Drop foreign key if exists
        fk_name = f'fk_{table}_user_id'
        if fk_name in existing_fks:
            op.drop_constraint(fk_name, table_name=table, type_='foreignkey')

        # Optionally rename 'user_id' back to 'userid' if needed
        if 'user_id' in columns and 'userid' not in columns:
            op.alter_column(table, 'user_id', new_column_name='userid')

        # Drop column if exists
        if 'user_id' in columns:
            op.drop_column(table, 'user_id')

    # Revert emigration_required to String
    op.alter_column(
        'travel_requisition_history',
        'emigration_required',
        type_=sa.String(),
        existing_type=sa.Boolean(),
        existing_nullable=True,
        postgresql_using="emigration_required::text"
    )