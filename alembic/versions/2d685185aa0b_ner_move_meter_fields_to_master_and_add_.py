"""ner move meter fields to master and add logs

Revision ID: 2d685185aa0b
Revises: b86822a7860d
Create Date: 2026-02-26 13:32:32.301011

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2d685185aa0b'
down_revision: Union[str, Sequence[str], None] = 'b86822a7860d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ===============================
    # MASTER ADD
    # ===============================
    op.add_column('ner_digital_logbook', sa.Column('dkn', sa.String(50)))
    op.add_column('ner_digital_logbook', sa.Column('hsn', sa.String(50)))
    op.add_column('ner_digital_logbook', sa.Column('mlr', sa.String(50)))
    op.add_column('ner_digital_logbook', sa.Column('sv3', sa.String(50)))
    op.add_column('ner_digital_logbook', sa.Column('sv4', sa.String(50)))
    op.add_column('ner_digital_logbook', sa.Column('technician_id', sa.Integer()))

    # ===============================
    # ENTRY TABLE
    # ===============================
    op.add_column('ner_digital_logbook_entry', sa.Column('logs', sa.Text()))

    op.drop_column('ner_digital_logbook_entry', 'dkn')
    op.drop_column('ner_digital_logbook_entry', 'hsn')
    op.drop_column('ner_digital_logbook_entry', 'mlr')
    op.drop_column('ner_digital_logbook_entry', 'sv3')
    op.drop_column('ner_digital_logbook_entry', 'sv4')

    # ===============================
    # HISTORY MASTER
    # ===============================
    op.add_column('ner_digital_logbook_history', sa.Column('dkn', sa.String(50)))
    op.add_column('ner_digital_logbook_history', sa.Column('hsn', sa.String(50)))
    op.add_column('ner_digital_logbook_history', sa.Column('mlr', sa.String(50)))
    op.add_column('ner_digital_logbook_history', sa.Column('sv3', sa.String(50)))
    op.add_column('ner_digital_logbook_history', sa.Column('sv4', sa.String(50)))
    op.add_column('ner_digital_logbook_history', sa.Column('technician_id', sa.Integer()))

    # ===============================
    # ENTRY HISTORY
    # ===============================
    op.add_column('ner_digital_logbook_entry_history', sa.Column('logs', sa.Text()))

    op.drop_column('ner_digital_logbook_entry_history', 'dkn')
    op.drop_column('ner_digital_logbook_entry_history', 'hsn')
    op.drop_column('ner_digital_logbook_entry_history', 'mlr')
    op.drop_column('ner_digital_logbook_entry_history', 'sv3')
    op.drop_column('ner_digital_logbook_entry_history', 'sv4')



def downgrade() -> None:
    """Downgrade schema."""
    pass
