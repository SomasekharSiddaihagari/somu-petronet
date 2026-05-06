"""Update TravelRequisition and add FK to users

Revision ID: 3538875544df
Revises: 0070bd141d19
Create Date: 2025-12-09 17:47:45.708652

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = '3538875544df'
down_revision: Union[str, Sequence[str], None] = '0070bd141d19'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # --------------------------------------------------------
    # 1. Convert String → Boolean safely using a temp column
    # --------------------------------------------------------

    # Step 1: Add new boolean column temporarily
    op.add_column(
        "travel_requisition",
        sa.Column("emigration_required_new", sa.Boolean(), nullable=True)
    )

    # Step 2: Copy/convert old string values to boolean
    conn = op.get_bind()
    conn.execute(text("""
        UPDATE travel_requisition
        SET emigration_required_new =
            CASE
                WHEN LOWER(emigration_required) IN ('yes', 'true', '1') THEN TRUE
                WHEN LOWER(emigration_required) IN ('no', 'false', '0') THEN FALSE
                ELSE NULL
            END
    """))

    # Step 3: Drop old column
    with op.batch_alter_table("travel_requisition") as batch_op:
        batch_op.drop_column("emigration_required")

    # Step 4: Rename new column → original name
    with op.batch_alter_table("travel_requisition") as batch_op:
        batch_op.alter_column(
            "emigration_required_new",
            new_column_name="emigration_required"
        )

    # --------------------------------------------------------
    # 2. Add user_id FK → users.user_id
    # --------------------------------------------------------
    op.add_column(
        "travel_requisition",
        sa.Column("user_id", sa.Integer(), nullable=True)
    )

    op.create_foreign_key(
        "fk_travel_requisition_user",
        source_table="travel_requisition",
        referent_table="users",
        local_cols=["user_id"],
        remote_cols=["user_id"],
        ondelete="SET NULL"
    )


def downgrade():
    # --------------------------------------------------------
    # 1. Drop FK + user_id
    # --------------------------------------------------------
    op.drop_constraint(
        "fk_travel_requisition_user",
        table_name="travel_requisition",
        type_="foreignkey"
    )
    op.drop_column("travel_requisition", "user_id")

    # --------------------------------------------------------
    # 2. Revert Boolean → String(10)
    # --------------------------------------------------------
    op.add_column(
        "travel_requisition",
        sa.Column("emigration_required_old", sa.String(length=10), nullable=True)
    )

    conn = op.get_bind()
    conn.execute(text("""
        UPDATE travel_requisition
        SET emigration_required_old =
            CASE
                WHEN emigration_required = TRUE THEN 'Yes'
                WHEN emigration_required = FALSE THEN 'No'
                ELSE NULL
            END
    """))

    with op.batch_alter_table("travel_requisition") as batch_op:
        batch_op.drop_column("emigration_required")

    with op.batch_alter_table("travel_requisition") as batch_op:
        batch_op.alter_column(
            "emigration_required_old",
            new_column_name="emigration_required"
        )