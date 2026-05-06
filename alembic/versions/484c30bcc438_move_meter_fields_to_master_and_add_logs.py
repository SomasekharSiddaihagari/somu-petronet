"""move meter fields to master and add logs

Revision ID: 484c30bcc438
Revises: 7d5e4ee81128
Create Date: 2026-02-26 12:46:25.593385

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '484c30bcc438'
down_revision: Union[str, Sequence[str], None] = '7d5e4ee81128'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ===============================
    # MASTER TABLE ADD
    # ===============================
    op.add_column('dkn_digital_logbook', sa.Column('hsn', sa.String(50)))
    op.add_column('dkn_digital_logbook', sa.Column('ner', sa.String(50)))
    op.add_column('dkn_digital_logbook', sa.Column('mlr', sa.String(50)))
    op.add_column('dkn_digital_logbook', sa.Column('svb', sa.String(50)))
    op.add_column('dkn_digital_logbook', sa.Column('ip1', sa.String(50)))
    op.add_column('dkn_digital_logbook', sa.Column('sv9', sa.String(50)))
    op.add_column('dkn_digital_logbook', sa.Column('sv10', sa.String(50)))
    op.add_column('dkn_digital_logbook', sa.Column('technician_id', sa.Integer()))

    # ===============================
    # ENTRY TABLE
    # ===============================
    op.add_column('dkn_digital_logbook_entry', sa.Column('logs', sa.Text()))

    # 🔥 DROP MOVED FIELDS FROM ENTRY
    op.drop_column('dkn_digital_logbook_entry', 'hsn')
    op.drop_column('dkn_digital_logbook_entry', 'ner')
    op.drop_column('dkn_digital_logbook_entry', 'mlr')
    op.drop_column('dkn_digital_logbook_entry', 'svb')
    op.drop_column('dkn_digital_logbook_entry', 'ip1')
    op.drop_column('dkn_digital_logbook_entry', 'sv9')
    op.drop_column('dkn_digital_logbook_entry', 'sv10')

    # ===============================
    # HISTORY MASTER
    # ===============================
    op.add_column('dkn_digital_logbook_history', sa.Column('hsn', sa.String(50)))
    op.add_column('dkn_digital_logbook_history', sa.Column('ner', sa.String(50)))
    op.add_column('dkn_digital_logbook_history', sa.Column('mlr', sa.String(50)))
    op.add_column('dkn_digital_logbook_history', sa.Column('svb', sa.String(50)))
    op.add_column('dkn_digital_logbook_history', sa.Column('ip1', sa.String(50)))
    op.add_column('dkn_digital_logbook_history', sa.Column('sv9', sa.String(50)))
    op.add_column('dkn_digital_logbook_history', sa.Column('sv10', sa.String(50)))
    op.add_column('dkn_digital_logbook_history', sa.Column('technician_id', sa.Integer()))

    # ===============================
    # ENTRY HISTORY
    # ===============================
    op.add_column('dkn_digital_logbook_entry_history', sa.Column('logs', sa.Text()))

    op.drop_column('dkn_digital_logbook_entry_history', 'hsn')
    op.drop_column('dkn_digital_logbook_entry_history', 'ner')
    op.drop_column('dkn_digital_logbook_entry_history', 'mlr')
    op.drop_column('dkn_digital_logbook_entry_history', 'svb')
    op.drop_column('dkn_digital_logbook_entry_history', 'ip1')
    op.drop_column('dkn_digital_logbook_entry_history', 'sv9')
    op.drop_column('dkn_digital_logbook_entry_history', 'sv10')



def downgrade() -> None:
    """Downgrade schema."""
    pass
