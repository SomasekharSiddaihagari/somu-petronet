"""remove education fields from users

Revision ID: ffcdc4cca8ef
Revises: ee30558b4565
Create Date: 2025-11-26 16:11:53.989911

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ffcdc4cca8ef'
down_revision: Union[str, Sequence[str], None] = 'ee30558b4565'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # ----- users table -----
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_column("qualification")
        batch_op.drop_column("year_of_completion")
        batch_op.drop_column("education_document")
 
    # ----- users_history table -----
    with op.batch_alter_table("users_history") as batch_op:
        batch_op.drop_column("qualification")
        batch_op.drop_column("year_of_completion")
        batch_op.drop_column("education_document")
 
 
def downgrade():
    # Recreate columns if rollback is needed
 
    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(sa.Column("qualification", sa.String(), nullable=True))
        batch_op.add_column(sa.Column("year_of_completion", sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column("education_document", sa.String(), nullable=True))
 
    with op.batch_alter_table("users_history") as batch_op:
        batch_op.add_column(sa.Column("qualification", sa.String(), nullable=True))
        batch_op.add_column(sa.Column("year_of_completion", sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column("education_document", sa.String(), nullable=True))