"""hsn move meter fields to master and add logs

Revision ID: b86822a7860d
Revises: 5425e8fe314c
Create Date: 2026-02-26 13:02:47.698925

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b86822a7860d'
down_revision: Union[str, Sequence[str], None] = '5425e8fe314c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ===============================
    # MASTER ADD
    # ===============================
    op.add_column('hsn_digital_logbook', sa.Column('dkn', sa.String(50)))
    op.add_column('hsn_digital_logbook', sa.Column('ner', sa.String(50)))
    op.add_column('hsn_digital_logbook', sa.Column('mlr', sa.String(50)))
    op.add_column('hsn_digital_logbook', sa.Column('sv5', sa.String(50)))
    op.add_column('hsn_digital_logbook', sa.Column('sv6', sa.String(50)))
    op.add_column('hsn_digital_logbook', sa.Column('sv7', sa.String(50)))
    op.add_column('hsn_digital_logbook', sa.Column('technician_id', sa.Integer()))

    # ===============================
    # ENTRY TABLE
    # ===============================
    op.add_column('hsn_digital_logbook_entry', sa.Column('logs', sa.Text()))

    op.drop_column('hsn_digital_logbook_entry', 'dkn')
    op.drop_column('hsn_digital_logbook_entry', 'ner')
    op.drop_column('hsn_digital_logbook_entry', 'mlr')
    op.drop_column('hsn_digital_logbook_entry', 'sv5')
    op.drop_column('hsn_digital_logbook_entry', 'sv6')
    op.drop_column('hsn_digital_logbook_entry', 'sv7')

    # ===============================
    # HISTORY MASTER
    # ===============================
    op.add_column('hsn_digital_logbook_history', sa.Column('dkn', sa.String(50)))
    op.add_column('hsn_digital_logbook_history', sa.Column('ner', sa.String(50)))
    op.add_column('hsn_digital_logbook_history', sa.Column('mlr', sa.String(50)))
    op.add_column('hsn_digital_logbook_history', sa.Column('sv5', sa.String(50)))
    op.add_column('hsn_digital_logbook_history', sa.Column('sv6', sa.String(50)))
    op.add_column('hsn_digital_logbook_history', sa.Column('sv7', sa.String(50)))
    op.add_column('hsn_digital_logbook_history', sa.Column('technician_id', sa.Integer()))

    # ===============================
    # ENTRY HISTORY
    # ===============================
    op.add_column('hsn_digital_logbook_entry_history', sa.Column('logs', sa.Text()))

    op.drop_column('hsn_digital_logbook_entry_history', 'dkn')
    op.drop_column('hsn_digital_logbook_entry_history', 'ner')
    op.drop_column('hsn_digital_logbook_entry_history', 'mlr')
    op.drop_column('hsn_digital_logbook_entry_history', 'sv5')
    op.drop_column('hsn_digital_logbook_entry_history', 'sv6')
    op.drop_column('hsn_digital_logbook_entry_history', 'sv7')



def downgrade() -> None:
    """Downgrade schema."""
    pass
