"""Add FK user_id to hr_leave_application

Revision ID: 50127e9d9117
Revises: 4f3a771efd20
Create Date: 2025-12-08 10:31:28.784773

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50127e9d9117'
down_revision: Union[str, Sequence[str], None] = '4f3a771efd20'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Ensure column exists
   
    # Add ForeignKey constraint safely
    op.create_foreign_key(
        'fk_hr_leave_application_user',        # constraint name
        'hr_leave_application',               # source table
        'users',                              # target table
        ['user_id'],                          # source column
        ['user_id'],                          # target column
        ondelete='SET NULL'                   # safe behavior if user deleted
    )
 
 
def downgrade():
    # Drop FK first (required by PostgreSQL)
    op.drop_constraint(
        'fk_hr_leave_application_user',
        'hr_leave_application',
        type_='foreignkey'
    )
 
    # Optional: drop column only if you want rollback fully
    op.drop_column('hr_leave_application', 'user_id')