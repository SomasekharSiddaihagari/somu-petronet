"""Update HIRAEntry: drop moc_request_no and change risk_level to String

Revision ID: 2a3ef39dfc77
Revises: 0d37cd28ac32
Create Date: 2025-11-01 17:35:56.291602

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '2a3ef39dfc77'
down_revision: Union[str, Sequence[str], None] = '0d37cd28ac32'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ✅ Drop moc_request_no column if it exists
    with op.batch_alter_table('hira_entries', schema=None) as batch_op:
        # Only drop if the column exists
        conn = op.get_bind()
        inspector = sa.inspect(conn)
        columns = [col['name'] for col in inspector.get_columns('hira_entries')]
        if 'moc_request_no' in columns:
            batch_op.drop_column('moc_request_no')

    # ✅ Convert Enum to String (safe data migration)
    # Rename old column temporarily
    with op.batch_alter_table('hira_entries', schema=None) as batch_op:
        batch_op.alter_column(
            'risk_level',
            existing_type=sa.Enum('Low', 'Medium', 'High', 'Critical', name='risklevelenum'),
            type_=sa.String(length=50),
            existing_nullable=False
        )


def downgrade():
    # Optional: revert String back to Enum if needed
    risk_enum = sa.Enum('Low', 'Medium', 'High', 'Critical', name='risklevelenum')
    with op.batch_alter_table('hira_entries', schema=None) as batch_op:
        batch_op.alter_column(
            'risk_level',
            existing_type=sa.String(length=50),
            type_=risk_enum,
            existing_nullable=False
        )

    # Recreate dropped column (if you ever rollback)
    with op.batch_alter_table('hira_entries', schema=None) as batch_op:
        batch_op.add_column(sa.Column('moc_request_no', sa.Integer(), nullable=True))