"""create users history with trigger

Revision ID: 6c7da82adac2
Revises: 4f2a787f8f54
Create Date: 2025-11-25 14:56:36.472169

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6c7da82adac2'
down_revision: Union[str, Sequence[str], None] = '4f2a787f8f54'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Create table
    op.create_table(
        'users_history',
        sa.Column('history_id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer),
        sa.Column('username', sa.String),
        sa.Column('hashed_password', sa.String),
        sa.Column('role_id', sa.Integer),
        sa.Column('station_id', sa.Integer),
        sa.Column('first_name', sa.String),
        sa.Column('last_name', sa.String),
        sa.Column('gender', sa.String),
        sa.Column('contact_phone', sa.String),
        sa.Column('emergency_mobile', sa.String),
        sa.Column('email', sa.String),
        sa.Column('personal_email', sa.String),
        sa.Column('employee_code', sa.String),
        sa.Column('designation', sa.String),
        sa.Column('station', sa.String),
        sa.Column('grade', sa.String),
        sa.Column('supervisor_id', sa.Integer),
        sa.Column('sap_loacation_code', sa.String),
        sa.Column('employment_type', sa.String),
 
        sa.Column('date_of_joining', sa.Date),
        sa.Column('dob', sa.Date),
        sa.Column('probation_from', sa.Date),
        sa.Column('probation_to', sa.Date),
        sa.Column('permanent_from', sa.Date),
 
        sa.Column('current_address', sa.Text),
        sa.Column('current_address_proof', sa.String),
        sa.Column('permanent_address', sa.Text),
        sa.Column('permanent_address_proof', sa.String),
 
        sa.Column('qualification', sa.String),
        sa.Column('year_of_completion', sa.Integer),
        sa.Column('education_document', sa.String),
 
        sa.Column('aadhaar', sa.String),
        sa.Column('aadhaar_file', sa.String),
        sa.Column('pan', sa.String),
        sa.Column('pan_file', sa.String),
        sa.Column('driving_license', sa.String),
        sa.Column('driving_license_file', sa.String),
        sa.Column('passport', sa.String),
        sa.Column('passport_file', sa.String),
 
        sa.Column('bank_name', sa.String),
        sa.Column('branch_name', sa.String),
        sa.Column('account_number', sa.String),
        sa.Column('ifsc_code', sa.String),
        sa.Column('account_holder_name', sa.String),
        sa.Column('account_type', sa.String),
        sa.Column('cancelled_cheque', sa.String),
 
        sa.Column('created_by', sa.String),
        sa.Column('created_date', sa.DateTime),
        sa.Column('modified_by', sa.String),
        sa.Column('modified_date', sa.DateTime),
        sa.Column('is_deleted', sa.Boolean),
 
        sa.Column('history_created_at', sa.DateTime, server_default=sa.text('now()'))
    )
 
    # Trigger function
    op.execute("""
    CREATE OR REPLACE FUNCTION insert_users_history()
    RETURNS TRIGGER AS $$
    BEGIN
        INSERT INTO users_history SELECT NEW.*, now();
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """)
 
    # Trigger
    op.execute("""
    CREATE TRIGGER trg_users_history
    AFTER INSERT ON users
    FOR EACH ROW EXECUTE FUNCTION insert_users_history();
    """)
 
 
def downgrade():
    op.execute("DROP TRIGGER IF EXISTS trg_users_history ON users;")
    op.execute("DROP FUNCTION IF EXISTS insert_users_history();")
    op.drop_table('users_history')
