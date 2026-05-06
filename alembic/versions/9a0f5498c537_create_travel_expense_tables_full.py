"""Create Travel Expense Tables Full

Revision ID: 9a0f5498c537
Revises: 407afabad954
Create Date: 2025-12-08 17:11:17.389499

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a0f5498c537'
down_revision: Union[str, Sequence[str], None] = '407afabad954'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
 
    # MAIN TABLE
    op.create_table(
        'travel_expense_sheet',
        sa.Column('tes_id', sa.BigInteger(), primary_key=True),
        sa.Column('requisition_number', sa.String(50), nullable=True),
 
        sa.Column('employee_name', sa.String(150), nullable=True),
        sa.Column('employee_number', sa.String(50), nullable=True),
        sa.Column('designation', sa.String(100), nullable=True),
        sa.Column('grade', sa.String(50), nullable=True),
        sa.Column('station', sa.String(100), nullable=True),
        sa.Column('department', sa.String(100), nullable=True),
        sa.Column('purpose_of_travel', sa.Text(), nullable=True),
 
        sa.Column('total_excl_gst', sa.Numeric(12, 2), nullable=True),
        sa.Column('total_gst', sa.Numeric(12, 2), nullable=True),
        sa.Column('total_incl_gst', sa.Numeric(12, 2), nullable=True),
        sa.Column('advance_taken', sa.Numeric(12, 2), nullable=True),
        sa.Column('amount_payable_receivable', sa.Numeric(12, 2), nullable=True),
 
        sa.Column('comments', sa.Text(), nullable=True),
        sa.Column('status', sa.String(50), nullable=True),
 
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now())
    )
 
    # CHILD TABLE
    op.create_table(
        'travel_expense_sheet_detail',
        sa.Column('tesd_id', sa.BigInteger(), primary_key=True),
        sa.Column('expense_sheet_id', sa.BigInteger(), sa.ForeignKey('travel_expense_sheet.tes_id'), nullable=True),
 
        sa.Column('date', sa.Date(), nullable=True),
        sa.Column('travel_route', sa.String(255), nullable=True),
 
        sa.Column('air_rail_bus_amount', sa.Numeric(12, 2), nullable=True),
        sa.Column('air_rail_bus_gst', sa.Numeric(12, 2), nullable=True),
        sa.Column('air_rail_bus_total', sa.Numeric(12, 2), nullable=True),
 
        sa.Column('hotel_amount', sa.Numeric(12, 2), nullable=True),
        sa.Column('hotel_gst', sa.Numeric(12, 2), nullable=True),
        sa.Column('hotel_total', sa.Numeric(12, 2), nullable=True),
 
        sa.Column('daily_allowance_amount', sa.Numeric(12, 2), nullable=True),
        sa.Column('daily_allowance_gst', sa.Numeric(12, 2), nullable=True),
        sa.Column('daily_allowance_total', sa.Numeric(12, 2), nullable=True),
 
        sa.Column('local_conveyance_amount', sa.Numeric(12, 2), nullable=True),
        sa.Column('local_conveyance_gst', sa.Numeric(12, 2), nullable=True),
        sa.Column('local_conveyance_total', sa.Numeric(12, 2), nullable=True),
 
        sa.Column('other_amount', sa.Numeric(12, 2), nullable=True),
        sa.Column('other_gst', sa.Numeric(12, 2), nullable=True),
        sa.Column('other_total', sa.Numeric(12, 2), nullable=True),
 
        sa.Column('air_rail_bus_proof', sa.String(255), nullable=True),
        sa.Column('hotel_proof', sa.String(255), nullable=True),
        sa.Column('daily_allowance_proof', sa.String(255), nullable=True),
        sa.Column('local_conveyance_proof', sa.String(255), nullable=True),
        sa.Column('other_proof', sa.String(255), nullable=True),
 
        sa.Column('remarks', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )
 
    # HISTORY MAIN
    op.create_table(
        'travel_expense_sheet_history',
        sa.Column('history_id', sa.BigInteger(), primary_key=True),
        sa.Column('expense_sheet_id', sa.BigInteger(), nullable=True),
        sa.Column('requisition_number', sa.String(50), nullable=True),
 
        sa.Column('employee_name', sa.String(150), nullable=True),
        sa.Column('employee_number', sa.String(50), nullable=True),
        
        sa.Column('grade', sa.String(50), nullable=True),
        sa.Column('station', sa.String(100), nullable=True),
        sa.Column('department', sa.String(100), nullable=True),
        sa.Column('purpose_of_travel', sa.Text(), nullable=True),
 
        sa.Column('total_excl_gst', sa.Numeric(12, 2), nullable=True),
        sa.Column('total_gst', sa.Numeric(12, 2), nullable=True),
        sa.Column('total_incl_gst', sa.Numeric(12, 2), nullable=True),
        sa.Column('advance_taken', sa.Numeric(12, 2), nullable=True),
        sa.Column('amount_payable_receivable', sa.Numeric(12, 2), nullable=True),
 
        sa.Column('comments', sa.Text(), nullable=True),
        sa.Column('status', sa.String(50), nullable=True),
 
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )
 
    # HISTORY DETAIL
    op.create_table(
        'travel_expense_sheet_detail_history',
        sa.Column('history_id', sa.BigInteger(), primary_key=True),
        sa.Column('expense_sheet_id', sa.BigInteger(), nullable=True),
        sa.Column('date', sa.Date(), nullable=True),
        sa.Column('travel_route', sa.String(255), nullable=True),
 
        sa.Column('air_rail_bus_amount', sa.Numeric(12, 2), nullable=True),
        sa.Column('air_rail_bus_gst', sa.Numeric(12, 2), nullable=True),
        sa.Column('air_rail_bus_total', sa.Numeric(12, 2), nullable=True),
 
        sa.Column('hotel_amount', sa.Numeric(12, 2), nullable=True),
        sa.Column('hotel_gst', sa.Numeric(12, 2), nullable=True),
        sa.Column('hotel_total', sa.Numeric(12, 2), nullable=True),
 
        sa.Column('daily_allowance_amount', sa.Numeric(12, 2), nullable=True),
        sa.Column('daily_allowance_gst', sa.Numeric(12, 2), nullable=True),
        sa.Column('daily_allowance_total', sa.Numeric(12, 2), nullable=True),
 
        sa.Column('local_conveyance_amount', sa.Numeric(12, 2), nullable=True),
        sa.Column('local_conveyance_gst', sa.Numeric(12, 2), nullable=True),
        sa.Column('local_conveyance_total', sa.Numeric(12, 2), nullable=True),
 
        sa.Column('other_amount', sa.Numeric(12, 2), nullable=True),
        sa.Column('other_gst', sa.Numeric(12, 2), nullable=True),
        sa.Column('other_total', sa.Numeric(12, 2), nullable=True),
 
        sa.Column('air_rail_bus_proof', sa.String(255), nullable=True),
        sa.Column('hotel_proof', sa.String(255), nullable=True),
        sa.Column('daily_allowance_proof', sa.String(255), nullable=True),
        sa.Column('local_conveyance_proof', sa.String(255), nullable=True),
        sa.Column('other_proof', sa.String(255), nullable=True),
        
        sa.Column('remarks', sa.Text(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )
 
 
def downgrade():
    op.drop_table('travel_expense_sheet_detail_history')
    op.drop_table('travel_expense_sheet_history')
    op.drop_table('travel_expense_sheet_detail')
    op.drop_table('travel_expense_sheet')