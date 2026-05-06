"""create employee_family_history

Revision ID: 6881d7d2f573
Revises: e527c3b97e60
Create Date: 2025-11-25 15:58:02.950134

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6881d7d2f573'
down_revision: Union[str, Sequence[str], None] = 'e527c3b97e60'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

 
 
def upgrade():

    op.create_table(

        "employee_family_history",

        sa.Column("history_id", sa.Integer, primary_key=True),
 
        sa.Column("ef_id", sa.Integer),

        sa.Column("user_id", sa.Integer),
 
        sa.Column("relation", sa.String),

        sa.Column("full_name", sa.String),

        sa.Column("dob", sa.Date),

        sa.Column("document", sa.String),
 
        sa.Column("history_created_at", sa.DateTime)

    )
 
 
def downgrade():

    op.drop_table("employee_family_history")

 