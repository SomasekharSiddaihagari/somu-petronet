"""mlr move meter fields to master and add logs

Revision ID: d2893aa6a575
Revises: 2d685185aa0b
Create Date: 2026-02-26 13:40:58.379146

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd2893aa6a575'
down_revision: Union[str, Sequence[str], None] = '2d685185aa0b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ===============================
    # MASTER ADD
    # ===============================
    op.add_column('mlr_digital_logbook', sa.Column('dkn', sa.String(50)))
    op.add_column('mlr_digital_logbook', sa.Column('hsn', sa.String(50)))
    op.add_column('mlr_digital_logbook', sa.Column('ner', sa.String(50)))
    op.add_column('mlr_digital_logbook', sa.Column('sv1', sa.String(50)))
    op.add_column('mlr_digital_logbook', sa.Column('sv2', sa.String(50)))
    op.add_column('mlr_digital_logbook', sa.Column('technician_id', sa.Integer()))

    # ===============================
    # ENTRY TABLE
    # ===============================
    op.add_column('mlr_digital_logbook_entry', sa.Column('logs', sa.Text()))

    op.drop_column('mlr_digital_logbook_entry', 'dkn')
    op.drop_column('mlr_digital_logbook_entry', 'hsn')
    op.drop_column('mlr_digital_logbook_entry', 'ner')
    op.drop_column('mlr_digital_logbook_entry', 'sv1')
    op.drop_column('mlr_digital_logbook_entry', 'sv2')

    # ===============================
    # HISTORY MASTER
    # ===============================
    op.add_column('mlr_digital_logbook_history', sa.Column('dkn', sa.String(50)))
    op.add_column('mlr_digital_logbook_history', sa.Column('hsn', sa.String(50)))
    op.add_column('mlr_digital_logbook_history', sa.Column('ner', sa.String(50)))
    op.add_column('mlr_digital_logbook_history', sa.Column('sv1', sa.String(50)))
    op.add_column('mlr_digital_logbook_history', sa.Column('sv2', sa.String(50)))
    op.add_column('mlr_digital_logbook_history', sa.Column('technician_id', sa.Integer()))

    # ===============================
    # ENTRY HISTORY
    # ===============================
    op.add_column('mlr_digital_logbook_entry_history', sa.Column('logs', sa.Text()))

    op.drop_column('mlr_digital_logbook_entry_history', 'dkn')
    op.drop_column('mlr_digital_logbook_entry_history', 'hsn')
    op.drop_column('mlr_digital_logbook_entry_history', 'ner')
    op.drop_column('mlr_digital_logbook_entry_history', 'sv1')
    op.drop_column('mlr_digital_logbook_entry_history', 'sv2')



def downgrade() -> None:
    """Downgrade schema."""
    pass
