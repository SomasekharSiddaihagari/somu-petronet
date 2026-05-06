"""rename supervisor_name to supervisor_id

Revision ID: 580afdbb416b
Revises: d72628418e57
Create Date: 2025-11-24 19:19:06.009153

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision: str = '580afdbb416b'
down_revision: Union[str, Sequence[str], None] = '541269591175'

branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    bind = op.get_bind()
    inspector = inspect(bind)

    columns = [col['name'] for col in inspector.get_columns('users')]

    # Step 1: Rename column only if it exists
    if "supervisor_name" in columns:
        op.alter_column(
            'users',
            'supervisor_name',
            new_column_name='supervisor_id'
        )

    # Step 2: Change datatype only if column exists after rename
    columns = [col['name'] for col in inspector.get_columns('users')]
    if "supervisor_id" in columns:
        op.execute("""
            ALTER TABLE users
            ALTER COLUMN supervisor_id TYPE INTEGER
            USING supervisor_id::INTEGER;
        """)

        # Step 3: Add UNIQUE constraint
        op.create_unique_constraint(
            'uq_users_supervisor_id',
            'users',
            ['supervisor_id']
        )

def downgrade():
    # Remove unique constraint
    op.drop_constraint('uq_users_supervisor_id', 'users', type_='unique')
 
    # Change type back to String
    op.alter_column(
        'users',
        'supervisor_id',
        type_=sa.String()
    )
 
    # Rename back to old name
    op.alter_column(
        'users',
        'supervisor_id',
        new_column_name='supervisor_name'
    )