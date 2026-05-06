"""Create Travel Requisition Tables

Revision ID: 407afabad954
Revises: 50127e9d9117
Create Date: 2025-12-08 12:29:28.405889

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '407afabad954'
down_revision: Union[str, Sequence[str], None] = '50127e9d9117'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    # Main

    op.create_table(

        'travel_requisition',

        sa.Column('travel_id', sa.BigInteger(), primary_key=True),

        sa.Column('employee_name', sa.String(150), nullable=True),

        sa.Column('employee_number', sa.String(50), nullable=True),

        sa.Column('designation', sa.String(100), nullable=True),

        sa.Column('grade', sa.String(100), nullable=True),

        sa.Column('station', sa.String(100), nullable=True),

        sa.Column('department', sa.String(100), nullable=True),

        sa.Column('purpose_of_travel', sa.Text(), nullable=True),

        sa.Column('visa_for', sa.Text(), nullable=True),

        sa.Column('emigration_required', sa.String(10), nullable=True),

        sa.Column('foreign_exchange', sa.Text(), nullable=True),

        sa.Column('status', sa.String(50), nullable=True),

        sa.Column('approver_comments', sa.Text(), nullable=True),

        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),

        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now())

    )
 
    # Travel

    op.create_table(

        'travel_requisition_travel',

        sa.Column('trt_id', sa.BigInteger(), primary_key=True),

        sa.Column('requisition_id', sa.BigInteger(), sa.ForeignKey('travel_requisition.travel_id')),

        sa.Column('from_location', sa.String(100), nullable=True),

        sa.Column('to_location', sa.String(100), nullable=True),

        sa.Column('travel_date', sa.Date(), nullable=True),

        sa.Column('flight_train_number', sa.String(100), nullable=True),

        sa.Column('class_of_travel', sa.String(50), nullable=True),

        sa.Column('travel_remarks', sa.Text(), nullable=True),

        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now())

    )
 
    # Hotel

    op.create_table(

        'travel_requisition_hotel',

        sa.Column('trh_id', sa.BigInteger(), primary_key=True),

        sa.Column('requisition_id', sa.BigInteger(), sa.ForeignKey('travel_requisition.travel_id')),

        sa.Column('city', sa.String(100), nullable=True),

        sa.Column('hotel_name', sa.String(150), nullable=True),

        sa.Column('hotel_remarks', sa.Text(), nullable=True),

        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now())

    )
 
    # Car

    op.create_table(

        'travel_requisition_car',

        sa.Column('trc_id', sa.BigInteger(), primary_key=True),

        sa.Column('requisition_id', sa.BigInteger(), sa.ForeignKey('travel_requisition.travel_id')),

        sa.Column('city', sa.String(100), nullable=True),

        sa.Column('car_from', sa.String(100), nullable=True),

        sa.Column('car_to', sa.String(100), nullable=True),

        sa.Column('car_type', sa.String(100), nullable=True),

        sa.Column('car_remarks', sa.Text(), nullable=True),

        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now())

    )
 
    # History Tables

    op.create_table(

        'travel_requisition_history',

        sa.Column('history_id', sa.BigInteger(), primary_key=True),

        sa.Column('requisition_id', sa.BigInteger(), nullable=True),

        sa.Column('employee_name', sa.String(150), nullable=True),

        sa.Column('employee_number', sa.String(50), nullable=True),

        sa.Column('designation', sa.String(100), nullable=True),

        sa.Column('grade', sa.String(100), nullable=True),

        sa.Column('station', sa.String(100), nullable=True),

        sa.Column('department', sa.String(100), nullable=True),

        sa.Column('purpose_of_travel', sa.Text(), nullable=True),

        sa.Column('visa_for', sa.Text(), nullable=True),

        sa.Column('emigration_required', sa.String(10), nullable=True),

        sa.Column('foreign_exchange', sa.Text(), nullable=True),

        sa.Column('status', sa.String(50), nullable=True),

        sa.Column('approver_comments', sa.Text(), nullable=True),

        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now())

    )
 
    op.create_table(

        'travel_requisition_travel_history',

        sa.Column('history_id', sa.BigInteger(), primary_key=True),

        sa.Column('requisition_id', sa.BigInteger(), nullable=True),

        sa.Column('from_location', sa.String(100), nullable=True),

        sa.Column('to_location', sa.String(100), nullable=True),

        sa.Column('travel_date', sa.Date(), nullable=True),

        sa.Column('flight_train_number', sa.String(100), nullable=True),

        sa.Column('class_of_travel', sa.String(50), nullable=True),

        sa.Column('travel_remarks', sa.Text(), nullable=True),

        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now())

    )
 
    op.create_table(

        'travel_requisition_hotel_history',

        sa.Column('history_id', sa.BigInteger(), primary_key=True),

        sa.Column('requisition_id', sa.BigInteger(), nullable=True),

        sa.Column('city', sa.String(100), nullable=True),

        sa.Column('hotel_name', sa.String(150), nullable=True),

        sa.Column('hotel_remarks', sa.Text(), nullable=True),

        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now())

    )
 
    op.create_table(

        'travel_requisition_car_history',

        sa.Column('history_id', sa.BigInteger(), primary_key=True),

        sa.Column('requisition_id', sa.BigInteger(), nullable=True),

        sa.Column('city', sa.String(100), nullable=True),

        sa.Column('car_from', sa.String(100), nullable=True),

        sa.Column('car_to', sa.String(100), nullable=True),

        sa.Column('car_type', sa.String(100), nullable=True),

        sa.Column('car_remarks', sa.Text(), nullable=True),

        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now())

    )
 
 
def downgrade():

    op.drop_table('travel_requisition_car_history')

    op.drop_table('travel_requisition_hotel_history')

    op.drop_table('travel_requisition_travel_history')

    op.drop_table('travel_requisition_history')

    op.drop_table('travel_requisition_car')

    op.drop_table('travel_requisition_hotel')

    op.drop_table('travel_requisition_travel')

    op.drop_table('travel_requisition')

 