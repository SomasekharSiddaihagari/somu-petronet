"""tables of leave_enchasgment

Revision ID: bb77b17d42cf
Revises: e55250700fb0
Create Date: 2025-12-26 16:14:16.540097

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb77b17d42cf'
down_revision: Union[str, Sequence[str], None] = 'e55250700fb0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.create_table(
        "leave_encashment",
        sa.Column("leave_encashment_id", sa.BigInteger(), primary_key=True),
 
        sa.Column("encashment_ref_id", sa.String(50), nullable=True),
 
        sa.Column("employee_name", sa.String(150), nullable=True),
        sa.Column("employee_code", sa.String(50), nullable=True),
        sa.Column("designation", sa.String(100), nullable=True),
        sa.Column("station", sa.String(100), nullable=True),
        sa.Column("encashment_date", sa.Date(), nullable=True),
        sa.Column("leave_type", sa.String(50), nullable=True),
 
        sa.Column("el_encashable", sa.Numeric(10, 2), nullable=True),
        sa.Column("encash_el", sa.Numeric(10, 2), nullable=True),
        sa.Column("balance_as_on_date", sa.Numeric(10, 2), nullable=True),
 
        sa.Column("request_text", sa.Text(), nullable=True),
        sa.Column("declaration_accepted", sa.Boolean(), nullable=True),
 
        sa.Column("status", sa.String(30), nullable=True),
 
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_by", sa.Integer(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True)
    )
 
    op.create_table(
        "leave_encashment_history",
        sa.Column("leave_encashment_history_id", sa.BigInteger(), primary_key=True),
 
        sa.Column("leave_encashment_id", sa.BigInteger(), nullable=True),
        sa.Column("encashment_ref_id", sa.String(50), nullable=True),
 
        sa.Column("employee_name", sa.String(150), nullable=True),
        sa.Column("employee_code", sa.String(50), nullable=True),
        sa.Column("designation", sa.String(100), nullable=True),
        sa.Column("station", sa.String(100), nullable=True),
        sa.Column("encashment_date", sa.Date(), nullable=True),
        sa.Column("leave_type", sa.String(50), nullable=True),
 
        sa.Column("el_encashable", sa.Numeric(10, 2), nullable=True),
        sa.Column("encash_el", sa.Numeric(10, 2), nullable=True),
        sa.Column("balance_as_on_date", sa.Numeric(10, 2), nullable=True),
 
        sa.Column("request_text", sa.Text(), nullable=True),
        sa.Column("declaration_accepted", sa.Boolean(), nullable=True),
 
        sa.Column("status", sa.String(30), nullable=True),
 
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_by", sa.Integer(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True)
    )
 
 
def downgrade():
    op.drop_table("leave_encashment_history")
    op.drop_table("leave_encashment")