"""tables of change of enchasments

Revision ID: a98796e0523c
Revises: 1b6f6238ae96
Create Date: 2025-12-26 17:36:32.579812

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a98796e0523c'
down_revision: Union[str, Sequence[str], None] = '1b6f6238ae96'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



 
def upgrade():

    # --------------------------------------------------

    # 1. CREATE ENCASHMENT MAIN TABLE

    # --------------------------------------------------

    op.create_table(

        "encashment_main",

        sa.Column("encashment_main_id", sa.BigInteger(), primary_key=True),
 
        sa.Column("encashment_ref_id", sa.String(50), nullable=True),
 
        sa.Column("employee_name", sa.String(150), nullable=True),

        sa.Column("employee_code", sa.String(50), nullable=True),

        sa.Column("department", sa.String(100), nullable=True),

        sa.Column("designation", sa.String(100), nullable=True),

        sa.Column("station", sa.String(100), nullable=True),

        sa.Column("grade", sa.String(50), nullable=True),
        sa.Column("claim_module", sa.String(50), nullable=True),
 
        sa.Column("status", sa.String(30), nullable=True),
 
        sa.Column("created_by", sa.Integer(), nullable=True),

        sa.Column(

            "created_at",

            sa.DateTime(timezone=True),

            server_default=sa.func.now()

        ),

        sa.Column("updated_by", sa.Integer(), nullable=True),

        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),

    )
 
    # --------------------------------------------------

    # 2. CREATE ENCASHMENT MAIN HISTORY TABLE

    # --------------------------------------------------

    op.create_table(

        "encashment_main_history",

        sa.Column(

            "encashment_main_history_id",

            sa.BigInteger(),

            primary_key=True

        ),
 
        sa.Column("encashment_main_id", sa.BigInteger(), nullable=True),
 
        sa.Column("encashment_ref_id", sa.String(50), nullable=True),

        sa.Column("employee_name", sa.String(150), nullable=True),

        sa.Column("employee_code", sa.String(50), nullable=True),

        sa.Column("department", sa.String(100), nullable=True),

        sa.Column("designation", sa.String(100), nullable=True),

        sa.Column("station", sa.String(100), nullable=True),

        sa.Column("grade", sa.String(50), nullable=True),
        sa.Column("claim_module", sa.String(50), nullable=True),
 
        sa.Column("status", sa.String(30), nullable=True),
 
        sa.Column("created_by", sa.Integer(), nullable=True),

        sa.Column(

            "created_at",

            sa.DateTime(timezone=True),

            server_default=sa.func.now()

        ),

        sa.Column("updated_by", sa.Integer(), nullable=True),

        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),

    )
 
    # --------------------------------------------------

    # 3. ADD 1–1 LINK COLUMN TO leave_encashment

    # --------------------------------------------------

    with op.batch_alter_table("leave_encashment") as batch_op:

        batch_op.add_column(

            sa.Column("encashment_main_id", sa.BigInteger(), nullable=True)

        )
 
 
def downgrade():

    # --------------------------------------------------

    # REMOVE LINK COLUMN

    # --------------------------------------------------

    with op.batch_alter_table("leave_encashment") as batch_op:

        batch_op.drop_column("encashment_main_id")
 
    # --------------------------------------------------

    # DROP HISTORY + MAIN TABLES

    # --------------------------------------------------

    op.drop_table("encashment_main_history")

    op.drop_table("encashment_main")

 