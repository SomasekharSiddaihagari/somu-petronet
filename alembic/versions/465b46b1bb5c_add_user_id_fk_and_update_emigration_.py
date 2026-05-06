"""add user_id FK and update emigration_required

Revision ID: 465b46b1bb5c
Revises: 3538875544df
Create Date: 2025-12-10 12:41:16.698384

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision: str = '465b46b1bb5c'
down_revision: Union[str, Sequence[str], None] = '3538875544df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    tables = [
        "daily_allowance_sheet",
        "daily_allowance_sheet_history",
        "meal_allowance_sheet",
        "meal_allowance_sheet_history",
        "travel_expense_sheet",
        "travel_expense_sheet_history",
        "travel_requisition",
        "travel_requisition_history",
        "travel_requisition_hotel",
        "travel_requisition_hotel_history",
        "travel_requisition_travel",
        "travel_requisition_travel_history",
        "travel_requisition_car",
        "travel_requisition_car_history"
    ]

    conn = op.get_bind()
    inspector = inspect(conn)

    for table in tables:
        existing_columns = [c['name'] for c in inspector.get_columns(table)]
        if 'user_id' not in existing_columns:
            op.add_column(table, sa.Column('user_id', sa.Integer(), nullable=True))
            op.create_foreign_key(
                f'fk_{table}_user_id', table, 'users', ['user_id'], ['user_id']
            )

    # Alter column in TravelRequisitionHistory to Boolean
    op.alter_column(
        'travel_requisition_history',
        'emigration_required',
        type_=sa.Boolean(),
        existing_type=sa.String(),
        existing_nullable=True,
        postgresql_using="emigration_required::boolean"
    )


def downgrade():
    tables = [
        "daily_allowance_sheet",
        "daily_allowance_sheet_history",
        "meal_allowance_sheet",
        "meal_allowance_sheet_history",
        "travel_expense_sheet",
        "travel_expense_sheet_history",
        "travel_requisition",
        "travel_requisition_history",
        "travel_requisition_hotel",
        "travel_requisition_hotel_history",
        "travel_requisition_travel",
        "travel_requisition_travel_history",
        "travel_requisition_car",
        "travel_requisition_car_history"
    ]

    conn = op.get_bind()
    inspector = inspect(conn)

    for table in tables:
        existing_columns = [c['name'] for c in inspector.get_columns(table)]
        if 'user_id' in existing_columns:
            op.drop_constraint(f'fk_{table}_user_id', table_name=table, type_='foreignkey')
            op.drop_column(table, 'user_id')

    # Revert emigration_required back to String
    op.alter_column(
    'travel_requisition_history',
    'emigration_required',
    type_=sa.String(),
    existing_type=sa.Boolean(),
    existing_nullable=True,
    postgresql_using="emigration_required::text"
)
