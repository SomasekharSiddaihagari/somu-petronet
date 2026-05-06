"""meeting_id hst to slno

Revision ID: 3aa27244b8bb
Revises: a9a0f2dcffe4
Create Date: 2026-02-16 16:09:43.036735

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3aa27244b8bb'
down_revision: Union[str, Sequence[str], None] = 'a9a0f2dcffe4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

"""rename meeting_id to sl_no in safety committee tables

Revision ID: rename_meeting_id_to_sl_no
Revises: <put_previous_revision_id>
Create Date: 2026-02-16
"""

from alembic import op
import sqlalchemy as sa




def upgrade():
    # ---- safety_committee_members ----
    with op.batch_alter_table('safety_committee_members', schema=None) as batch_op:
        batch_op.alter_column(
            'meeting_id',
            new_column_name='sl_no',
            existing_type=sa.Integer(),
            existing_nullable=True
        )

    # ---- safety_committee_members_history ----
    with op.batch_alter_table('safety_committee_members_history', schema=None) as batch_op:
        batch_op.alter_column(
            'meeting_id',
            new_column_name='sl_no',
            existing_type=sa.Integer(),
            existing_nullable=True
        )


def downgrade():
    # ---- revert safety_committee_members ----
    with op.batch_alter_table('safety_committee_members', schema=None) as batch_op:
        batch_op.alter_column(
            'sl_no',
            new_column_name='meeting_id',
            existing_type=sa.Integer(),
            existing_nullable=True
        )

    # ---- revert safety_committee_members_history ----
    with op.batch_alter_table('safety_committee_members_history', schema=None) as batch_op:
        batch_op.alter_column(
            'sl_no',
            new_column_name='meeting_id',
            existing_type=sa.Integer(),
            existing_nullable=True
        )
