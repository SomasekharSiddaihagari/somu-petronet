"""Rename designation_grade and add grade column

Revision ID: f4ceb91c05dc
Revises: 1f6f6ef03d1d
Create Date: 2025-12-08 18:03:27.968251

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4ceb91c05dc'
down_revision: Union[str, Sequence[str], None] = '1f6f6ef03d1d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
 
    # MAIN TABLE
    op.create_table(
        'meal_allowance_sheet',
        sa.Column('meal_sheet_id', sa.BigInteger(), primary_key=True),
        sa.Column('requisition_number', sa.String(50), nullable=True),
 
        sa.Column('employee_name', sa.String(150), nullable=True),
        sa.Column('employee_number', sa.String(50), nullable=True),
        sa.Column('designation_grade', sa.String(100), nullable=True),
        sa.Column('grade', sa.String(50), nullable=True),
        sa.Column('station', sa.String(100), nullable=True),
        sa.Column('department', sa.String(100), nullable=True),
        sa.Column('purpose_of_travel', sa.Text(), nullable=True),
 
        sa.Column('total_excl_gst', sa.Numeric(12, 2), nullable=True),
        sa.Column('total_gst', sa.Numeric(12, 2), nullable=True),
        sa.Column('total_incl_gst', sa.Numeric(12, 2), nullable=True),
        sa.Column('advance_taken', sa.Numeric(12, 2), nullable=True),
        sa.Column('amount_receivable_payable', sa.Numeric(12, 2), nullable=True),
 
        sa.Column('comments', sa.Text(), nullable=True),
        sa.Column('status', sa.String(50), nullable=True),
 
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now())
    )
 
    # DETAIL TABLE
    op.create_table(
        'meal_allowance_sheet_detail',
        sa.Column('meal_sheet_detail_id', sa.BigInteger(), primary_key=True),
        sa.Column('meal_sheet_id', sa.BigInteger(), sa.ForeignKey('meal_allowance_sheet.meal_sheet_id'), nullable=True),
 
        sa.Column('date', sa.Date(), nullable=True),
        sa.Column('travel_route', sa.String(255), nullable=True),
        sa.Column('time_duration', sa.String(50), nullable=True),
        sa.Column('distance_from_station', sa.String(50), nullable=True),
        sa.Column('purpose', sa.Text(), nullable=True),
 
        sa.Column('meal_amount', sa.Numeric(12, 2), nullable=True),
        sa.Column('meal_gst', sa.Numeric(12, 2), nullable=True),
        sa.Column('meal_total', sa.Numeric(12, 2), nullable=True),
 
        sa.Column('meal_proof', sa.String(255), nullable=True),
        sa.Column('remarks', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )
 
    # HISTORY MAIN
    op.create_table(
        'meal_allowance_sheet_history',
        sa.Column('meal_sheet_history_id', sa.BigInteger(), primary_key=True),
        sa.Column('meal_sheet_id', sa.BigInteger(), nullable=True),
 
        sa.Column('requisition_number', sa.String(50), nullable=True),
        sa.Column('employee_name', sa.String(150), nullable=True),
        sa.Column('employee_number', sa.String(50), nullable=True),
        sa.Column('designation_grade', sa.String(100), nullable=True),
        sa.Column('grade', sa.String(50), nullable=True),
        sa.Column('station', sa.String(100), nullable=True),
        sa.Column('department', sa.String(100), nullable=True),
        sa.Column('purpose_of_travel', sa.Text(), nullable=True),
 
        sa.Column('total_excl_gst', sa.Numeric(12, 2), nullable=True),
        sa.Column('total_gst', sa.Numeric(12, 2), nullable=True),
        sa.Column('total_incl_gst', sa.Numeric(12, 2), nullable=True),
        sa.Column('advance_taken', sa.Numeric(12, 2), nullable=True),
        sa.Column('amount_receivable_payable', sa.Numeric(12, 2), nullable=True),
 
        sa.Column('comments', sa.Text(), nullable=True),
        sa.Column('status', sa.String(50), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )
 
    # HISTORY DETAIL
    op.create_table(
        'meal_allowance_sheet_detail_history',
        sa.Column('meal_sheet_detail_history_id', sa.BigInteger(), primary_key=True),
        sa.Column('meal_sheet_id', sa.BigInteger(), nullable=True),
 
        sa.Column('date', sa.Date(), nullable=True),
        sa.Column('travel_route', sa.String(255), nullable=True),
        sa.Column('time_duration', sa.String(50), nullable=True),
        sa.Column('distance_from_station', sa.String(50), nullable=True),
        sa.Column('purpose', sa.Text(), nullable=True),
 
        sa.Column('meal_amount', sa.Numeric(12, 2), nullable=True),
        sa.Column('meal_gst', sa.Numeric(12, 2), nullable=True),
        sa.Column('meal_total', sa.Numeric(12, 2), nullable=True),
 
        sa.Column('meal_proof', sa.String(255), nullable=True),
        sa.Column('remarks', sa.Text(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )
 
 
def downgrade():
    op.drop_table('meal_allowance_sheet_detail_history')
    op.drop_table('meal_allowance_sheet_history')
    op.drop_table('meal_allowance_sheet_detail')
    op.drop_table('meal_allowance_sheet')
